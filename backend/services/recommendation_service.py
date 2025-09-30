# Copyright (c) 2025 Bhagya Dissanayake
# All rights reserved. This code is proprietary and confidential.
# Unauthorized copying, distribution, or use is strictly prohibited.

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from services.data_service import data_service
import ast

class RecommendationService:
    def __init__(self):
        self.data_service = data_service
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.similarity_matrix = None
        self._build_similarity_matrix()
    
    def _build_similarity_matrix(self):
        """Build similarity matrix for content-based recommendations"""
        laptops = self.data_service.get_all_laptops()
        if not laptops:
            return
        
        # Create feature vectors for each laptop
        laptop_features = []
        for laptop in laptops:
            features = []
            
            # Extract text features
            features.append(str(laptop.get('Brand', '')))
            features.append(str(laptop.get('Model', '')))
            features.append(str(laptop.get('Processor', '')))
            features.append(str(laptop.get('Operating System', '')))
            features.append(str(laptop.get('Graphics', '')))
            features.append(str(laptop.get('Memory (RAM)', '')))
            features.append(str(laptop.get('Storage', '')))
            features.append(str(laptop.get('Display', '')))
            
            # Extract review sentiment
            try:
                review_detail = laptop.get('Review Details', '{}')
                if isinstance(review_detail, str):
                    review_dict = ast.literal_eval(review_detail)
                    features.append(str(review_dict.get('AI Summary', '')))
            except:
                pass
            
            laptop_features.append(' '.join(features))
        
        # Create TF-IDF matrix
        try:
            tfidf_matrix = self.vectorizer.fit_transform(laptop_features)
            self.similarity_matrix = cosine_similarity(tfidf_matrix)
        except Exception as e:
            print(f"Error building similarity matrix: {e}")
            self.similarity_matrix = None
    
    def get_content_based_recommendations(self, laptop_id: int, num_recommendations: int = 5) -> List[Dict]:
        """Get content-based recommendations for a laptop"""
        if self.similarity_matrix is None:
            return []
        
        laptops = self.data_service.get_all_laptops()
        if laptop_id >= len(laptops):
            return []
        
        # Get similarity scores for the given laptop
        similarity_scores = self.similarity_matrix[laptop_id]
        
        # Get top similar laptops (excluding the laptop itself)
        similar_indices = np.argsort(similarity_scores)[::-1][1:num_recommendations+1]
        
        recommendations = []
        for idx in similar_indices:
            laptop = laptops[idx]
            recommendations.append({
                'laptop_id': idx,
                'similarity_score': float(similarity_scores[idx]),
                'brand': laptop.get('Brand', ''),
                'model': laptop.get('Model', ''),
                'processor': laptop.get('Processor', ''),
                'memory': laptop.get('Memory (RAM)', ''),
                'storage': laptop.get('Storage', ''),
                'display': laptop.get('Display', ''),
                'price_details': laptop.get('Price Details', ''),
                'review_summary': self._extract_review_summary(laptop)
            })
        
        return recommendations
    
    def get_constraint_based_recommendations(self, constraints: Dict[str, Any]) -> List[Dict]:
        """Get recommendations based on user constraints"""
        print(f"DEBUG: Received constraints: {constraints}")
        laptops = self.data_service.get_all_laptops()
        print(f"DEBUG: Total laptops loaded: {len(laptops)}")
        scored_laptops = []
        
        for i, laptop in enumerate(laptops):
            # First check if laptop meets hard constraints (like max_price)
            if self._meets_hard_constraints(laptop, constraints):
                score = self._calculate_constraint_score(laptop, constraints)
                if score > 0:
                    scored_laptops.append({
                        'laptop_id': i,
                        'score': score,
                        'laptop': laptop
                    })
        
        # Sort by score and return top recommendations
        scored_laptops.sort(key=lambda x: x['score'], reverse=True)
        print(f"DEBUG: Laptops that passed hard constraints: {len(scored_laptops)}")
        
        recommendations = []
        for item in scored_laptops[:10]:  # Top 10
            laptop = item['laptop']
            
            # Use the already parsed price_details from data service
            price_details = laptop.get('price_details', {})
            
            # Parse availability
            availability = {}
            try:
                availability_str = laptop.get('Availability', '{}')
                if isinstance(availability_str, str):
                    availability = ast.literal_eval(availability_str)
            except:
                availability = {}
            
            # Parse promos
            promos = []
            try:
                promos_str = laptop.get('Promos / Offers', '[]')
                if isinstance(promos_str, str):
                    promos = ast.literal_eval(promos_str)
            except:
                promos = []
            
            # Clean up NaN values for JSON serialization
            def clean_value(value):
                import math
                import pandas as pd
                if pd.isna(value) or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
                    return None
                return value
            
            recommendations.append({
                'laptop_id': item['laptop_id'],
                'match_score': clean_value(item['score']),
                'brand': clean_value(laptop.get('Brand', '')),
                'model': clean_value(laptop.get('Model', '')),
                'processor': clean_value(laptop.get('Processor', '')),
                'memory': clean_value(laptop.get('Memory (RAM)', '')),
                'storage': clean_value(laptop.get('Storage', '')),
                'display': clean_value(laptop.get('Display', '')),
                'price_details': price_details,  # Now an object
                'availability': availability,    # Now an object
                'promos': promos,                # Now a list
                'review_summary': clean_value(self._extract_review_summary(laptop)),
                'match_reasons': self._get_match_reasons(laptop, constraints)
            })
        
        return recommendations
    
    def get_trending_laptops(self, limit: int = 5) -> List[Dict]:
        """Get trending laptops based on ratings and review counts"""
        laptops = self.data_service.get_all_laptops()
        trending = []
        
        for i, laptop in enumerate(laptops):
            try:
                review_detail = laptop.get('Review Details', '{}')
                if isinstance(review_detail, str):
                    review_dict = ast.literal_eval(review_detail)
                    
                    rating_str = review_dict.get('Overall Rating', '0/5')
                    rating = float(rating_str.split('/')[0])
                    
                    # Extract review count
                    review_text = review_dict.get('Overall Rating', '')
                    review_count = 0
                    if '(' in review_text and 'reviews' in review_text:
                        try:
                            count_str = review_text.split('(')[1].split(' ')[0]
                            review_count = int(count_str)
                        except:
                            pass
                    
                    # Calculate trending score (rating * log(review_count + 1))
                    trending_score = rating * np.log(review_count + 1)
                    
                    trending.append({
                        'laptop_id': i,
                        'trending_score': trending_score,
                        'rating': rating,
                        'review_count': review_count,
                        'brand': laptop.get('Brand', ''),
                        'model': laptop.get('Model', ''),
                        'processor': laptop.get('Processor', ''),
                        'price_details': laptop.get('Price Details', ''),
                        'review_summary': self._extract_review_summary(laptop)
                    })
            except:
                continue
        
        # Sort by trending score
        trending.sort(key=lambda x: x['trending_score'], reverse=True)
        return trending[:limit]
    
    def _calculate_constraint_score(self, laptop: Dict, constraints: Dict[str, Any]) -> float:
        """Calculate how well a laptop matches the given constraints"""
        score = 0.0
        
        # Brand preference
        brand_value = constraints.get('brand') or constraints.get('brand')
        if brand_value:
            if brand_value.lower() in laptop.get('Brand', '').lower():
                score += 10
        
        # Price constraint
        max_price_value = constraints.get('max_price') or constraints.get('maxPrice')
        if max_price_value:
            try:
                # Use the already parsed price_details from data service
                price_dict = laptop.get('price_details', {})
                current_price = price_dict.get('Current Price', 'Not Available')
                if current_price != 'Not Available':
                    price_str = str(current_price).replace('$', '').replace(',', '')
                    if price_str.replace('.', '').isdigit():
                        price = float(price_str)
                        max_price = float(max_price_value)
                        if price <= max_price:
                            # Higher score for lower prices (better value)
                            price_score = max(0, 10 - (price / max_price) * 5)
                            score += price_score
            except:
                pass
        
        # Rating constraint
        min_rating_value = constraints.get('min_rating') or constraints.get('minRating')
        if min_rating_value:
            try:
                # Use the already parsed review_details from data service
                review_dict = laptop.get('review_details', {})
                rating_str = review_dict.get('Overall Rating', '0/5')
                rating = float(rating_str.split('/')[0])
                min_rating = float(min_rating_value)
                if rating >= min_rating:
                    score += rating * 2  # Higher rating = higher score
            except:
                pass
        
        # Processor preference
        processor_value = constraints.get('processor_type') or constraints.get('processorType')
        if processor_value:
            processor = laptop.get('Processor', '').lower()
            if processor_value.lower() in processor:
                score += 5
        
        # Memory preference
        if 'min_memory' in constraints and constraints['min_memory']:
            memory = laptop.get('Memory (RAM)', '')
            if constraints['min_memory'].lower() in memory.lower():
                score += 3
        
        # Storage preference
        if 'storage_type' in constraints and constraints['storage_type']:
            storage = laptop.get('Storage', '').lower()
            if constraints['storage_type'].lower() in storage:
                score += 3
        
        return score
    
    def _meets_hard_constraints(self, laptop: Dict, constraints: Dict[str, Any]) -> bool:
        """Check if laptop meets hard constraints (must be met, not just scored)"""
        
        # Price constraint - must be within budget
        max_price_value = constraints.get('max_price') or constraints.get('maxPrice')
        if max_price_value:
            try:
                price_dict = laptop.get('price_details', {})
                current_price = price_dict.get('Current Price', 'Not Available')
                print(f"DEBUG: Laptop {laptop.get('Brand', '')} {laptop.get('Model', '')} - Price: {current_price}")
                
                if current_price != 'Not Available':
                    price_str = str(current_price).replace('$', '').replace(',', '')
                    if price_str.replace('.', '').isdigit():
                        price = float(price_str)
                        max_price = float(max_price_value)
                        print(f"DEBUG: Comparing price {price} vs max_price {max_price}")
                        if price > max_price:
                            print(f"DEBUG: Excluding laptop - price {price} > max_price {max_price}")
                            return False
                    else:
                        print(f"DEBUG: Price string '{price_str}' is not numeric")
                else:
                    print(f"DEBUG: Price is 'Not Available'")
            except Exception as e:
                print(f"DEBUG: Price parsing error: {e}")
                # If price parsing fails, exclude the laptop
                return False
        
        # Rating constraint - must meet minimum rating
        min_rating_value = constraints.get('min_rating') or constraints.get('minRating')
        if min_rating_value:
            try:
                review_dict = laptop.get('review_details', {})
                rating_str = review_dict.get('Overall Rating', '0/5')
                rating = float(rating_str.split('/')[0])
                min_rating = float(min_rating_value)
                if rating < min_rating:
                    return False
            except:
                # If rating parsing fails, exclude the laptop
                return False
        
        return True
    
    def _extract_review_summary(self, laptop: Dict) -> str:
        """Extract review summary from laptop data"""
        try:
            # Use the already parsed review_details from data service
            review_detail = laptop.get('review_details', {})
            if isinstance(review_detail, dict):
                return review_detail.get('AI Summary', 'No review summary available')
        except:
            pass
        return 'No review summary available'
    
    def _get_match_reasons(self, laptop: Dict, constraints: Dict[str, Any]) -> List[str]:
        """Get reasons why a laptop matches the constraints"""
        reasons = []
        
        brand_value = constraints.get('brand') or constraints.get('brand')
        if brand_value:
            if brand_value.lower() in laptop.get('Brand', '').lower():
                reasons.append(f"Matches preferred brand: {laptop.get('Brand', '')}")
        
        max_price_value = constraints.get('max_price') or constraints.get('maxPrice')
        if max_price_value:
            try:
                # Use the already parsed price_details from data service
                price_dict = laptop.get('price_details', {})
                current_price = price_dict.get('Current Price', 'Not Available')
                if current_price != 'Not Available':
                    reasons.append(f"Within budget: {current_price}")
            except:
                pass
        
        min_rating_value = constraints.get('min_rating') or constraints.get('minRating')
        if min_rating_value:
            try:
                # Use the already parsed review_details from data service
                review_dict = laptop.get('review_details', {})
                rating_str = review_dict.get('Overall Rating', '0/5')
                rating = float(rating_str.split('/')[0])
                min_rating = float(min_rating_value)
                if rating >= min_rating:
                    reasons.append(f"High rating: {rating_str}")
            except:
                pass
        
        return reasons

# Global instance
recommendation_service = RecommendationService()
