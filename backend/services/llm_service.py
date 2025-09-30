# Copyright (c) 2025 Bhagya Dissanayake
# All rights reserved. This code is proprietary and confidential.
# Unauthorized copying, distribution, or use is strictly prohibited.

import os
import requests
import json
from typing import Dict, List, Any, Optional
from services.data_service import data_service

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        
        # Debug info (can be removed in production)
        # print(f"DEBUG: API Key found: {bool(self.api_key)}")
        # print(f"DEBUG: API Key length: {len(self.api_key) if self.api_key else 0}")
        
        if not self.api_key:
            print("Warning: DEEPSEEK_API_KEY not found in environment variables")
    
    def _make_request(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000) -> Optional[str]:
        """Make a request to DeepSeek API"""
        # print(f"DEBUG: Making request with API key: {bool(self.api_key)}")
        
        if not self.api_key:
            return "Error: API key not configured"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            # print(f"DEBUG: Making request to {self.base_url}/chat/completions")
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data)
            # print(f"DEBUG: Response status: {response.status_code}")
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"DEBUG: Request failed with error: {str(e)}")
            return f"Error: {str(e)}"
    
    def chat_query(self, user_query: str, context: str = "") -> Dict[str, Any]:
        """Handle chat queries about laptops"""
        
        # Get relevant laptop data for context
        laptops = data_service.get_all_laptops()
        
        # Search for specific laptop models mentioned in the query
        relevant_laptops = self._find_relevant_laptops(user_query, laptops)
        
        # If no specific laptops found, use first 5 as fallback
        if not relevant_laptops:
            relevant_laptops = laptops[:5]
        else:
            # Limit to avoid token limits while ensuring we include relevant ones
            relevant_laptops = relevant_laptops[:10]
        
        # Create context from relevant laptop data
        laptop_context = self._create_laptop_context(relevant_laptops)
        
        system_prompt = f"""You are a laptop expert assistant specializing in business laptops from Lenovo and HP. 

Available laptop data:
{laptop_context}

CRITICAL FORMATTING RULES:
1. ALWAYS use bullet points (•) for lists, NEVER paragraphs
2. Use numbered lists (1., 2., 3.) for step-by-step information
3. Keep each bullet point SHORT (1-2 lines max)
4. MINIMAL bold formatting - only use **bold** for main section titles snd laptop names
5. Maximum 200 words total
6. Format prices as $XXX
7. Use line breaks between sections
8. NO bold formatting for specs

EXAMPLES OF GOOD FORMATTING:
**Top Laptops Under $1000:**

**Lenovo ThinkPad E14 - $899**
  - Intel i5, 8GB RAM, 256GB SSD
  - Great for business use
**HP ProBook 440 - $799**
  - AMD Ryzen 5, 16GB RAM, 512GB SSD
  - Excellent value

**Key Differences:**
• ThinkPad: Better keyboard, more durable
• ProBook: Better price, more RAM

Answer user questions about laptops, specifications, comparisons, and recommendations."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        response = self._make_request(messages, temperature=0.7, max_tokens=300)
        # print(f"DEBUG: Got response: {response[:100]}...")
        
        # Clean up the response
        cleaned_response = self._clean_response(response)
        
        result = {
            "query": user_query,
            "response": cleaned_response,
            "context_used": laptop_context[:200] + "..." if len(laptop_context) > 200 else laptop_context,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        # print(f"DEBUG: Returning result with response type: {type(response)}")
        return result
    
    def get_recommendations(self, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Get laptop recommendations based on user constraints"""
        laptops = data_service.get_all_laptops()
        
        # Filter laptops based on constraints
        filtered_laptops = self._filter_laptops_by_constraints(laptops, constraints)
        
        # Create context for recommendations
        laptop_context = self._create_laptop_context(filtered_laptops[:10])
        
        constraints_str = self._format_constraints(constraints)
        
        system_prompt = f"""You are a laptop recommendation expert specializing in business laptops. Based on the user's constraints and available laptops, provide recommendations.

User constraints:
{constraints_str}

Available laptops:
{laptop_context}

Format your response as follows:
**Top Recommendations:**

**1. [Brand] [Model] - $[Price]**
• **Why it fits:** [Brief rationale]
• **Key specs:** [Processor, RAM, Storage, Display]
• **Pros:** [Main advantages]
• **Cons:** [Any drawbacks]

**2. [Brand] [Model] - $[Price]**
• **Why it fits:** [Brief rationale]
• **Key specs:** [Processor, RAM, Storage, Display]
• **Pros:** [Main advantages]
• **Cons:** [Any drawbacks]

[Continue for 3-5 recommendations]

**Summary:** [Brief overall recommendation based on their needs]

Keep each recommendation concise but informative."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please recommend laptops based on these constraints: {constraints_str}"}
        ]
        
        response = self._make_request(messages, temperature=0.8, max_tokens=1500)
        
        return {
            "constraints": constraints,
            "recommendations": response,
            "laptops_considered": len(filtered_laptops),
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    def _create_laptop_context(self, laptops: List[Dict]) -> str:
        """Create a text context from laptop data"""
        context_parts = []
        
        for i, laptop in enumerate(laptops):
            laptop_info = f"Laptop {i+1}:\n"
            laptop_info += f"Brand: {laptop.get('Brand', 'N/A')}\n"
            laptop_info += f"Model: {laptop.get('Model', 'N/A')}\n"
            laptop_info += f"Processor: {laptop.get('Processor', 'N/A')}\n"
            laptop_info += f"Memory: {laptop.get('Memory (RAM)', 'N/A')}\n"
            laptop_info += f"Storage: {laptop.get('Storage', 'N/A')}\n"
            laptop_info += f"Display: {laptop.get('Display', 'N/A')}\n"
            laptop_info += f"Price: {laptop.get('Price Details', 'N/A')}\n"
            laptop_info += f"Reviews: {laptop.get('Review Details', 'N/A')}\n"
            laptop_info += "---\n"
            
            context_parts.append(laptop_info)
        
        return "\n".join(context_parts)
    
    def _filter_laptops_by_constraints(self, laptops: List[Dict], constraints: Dict[str, Any]) -> List[Dict]:
        """Filter laptops based on user constraints"""
        filtered = laptops.copy()
        
        # Filter by brand
        if 'brand' in constraints and constraints['brand']:
            filtered = [l for l in filtered if constraints['brand'].lower() in l.get('Brand', '').lower()]
        
        # Filter by max price
        if 'max_price' in constraints and constraints['max_price']:
            max_price = float(constraints['max_price'])
            price_filtered = []
            for laptop in filtered:
                try:
                    price_detail = laptop.get('Price Details', '{}')
                    if isinstance(price_detail, str):
                        import ast
                        price_dict = ast.literal_eval(price_detail)
                        current_price = price_dict.get('Current Price', 'Not Available')
                        if current_price != 'Not Available':
                            price_str = str(current_price).replace('$', '').replace(',', '')
                            if price_str.replace('.', '').isdigit():
                                price = float(price_str)
                                if price <= max_price:
                                    price_filtered.append(laptop)
                except:
                    continue
            filtered = price_filtered
        
        # Filter by minimum rating
        if 'min_rating' in constraints and constraints['min_rating']:
            min_rating = float(constraints['min_rating'])
            rating_filtered = []
            for laptop in filtered:
                try:
                    review_detail = laptop.get('Review Details', '{}')
                    if isinstance(review_detail, str):
                        import ast
                        review_dict = ast.literal_eval(review_detail)
                        rating_str = review_dict.get('Overall Rating', '0/5')
                        rating = float(rating_str.split('/')[0])
                        if rating >= min_rating:
                            rating_filtered.append(laptop)
                except:
                    continue
            filtered = rating_filtered
        
        return filtered
    
    def _format_constraints(self, constraints: Dict[str, Any]) -> str:
        """Format constraints for display"""
        formatted = []
        for key, value in constraints.items():
            if value:
                formatted.append(f"{key.replace('_', ' ').title()}: {value}")
        return "\n".join(formatted)
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the LLM response for better display"""
        if not response or response.startswith("Error:"):
            return response
        
        # Remove excessive whitespace
        response = response.strip()
        
        # Fix common formatting issues
        response = response.replace('\n\n\n', '\n\n')  # Remove triple line breaks
        response = response.replace('  ', ' ')  # Remove double spaces
        
        # Convert various bullet styles to consistent bullet points
        response = response.replace('- ', '• ')
        response = response.replace('* ', '• ')
        response = response.replace('+ ', '• ')
        
        # Remove excessive bold formatting - only keep bold for main headings
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Remove bold formatting from bullet points and individual items
                if line.startswith('•'):
                    # Remove ** from laptop names and specs in bullet points
                    line = line.replace('**', '')
                elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
                    # Remove ** from numbered list items
                    line = line.replace('**', '')
                elif ':' in line and not line.startswith('**'):
                    # This might be a section heading, keep it as is
                    pass
                else:
                    # For other lines, remove excessive bold formatting
                    # Only keep bold if it's a clear section heading
                    if not (line.startswith('**') and line.endswith('**') and len(line) < 50):
                        line = line.replace('**', '')
                
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def _find_relevant_laptops(self, user_query: str, laptops: List[Dict]) -> List[Dict]:
        """Find laptops relevant to the user query"""
        query_lower = user_query.lower()
        relevant_laptops = []
        
        for laptop in laptops:
            brand = laptop.get('Brand', '').lower()
            model = laptop.get('Model', '').lower()
            
            # Check if brand and model are mentioned in the query
            if brand in query_lower and any(word in query_lower for word in model.split()):
                relevant_laptops.append(laptop)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_laptops = []
        for laptop in relevant_laptops:
            laptop_id = f"{laptop.get('Brand', '')} {laptop.get('Model', '')}"
            if laptop_id not in seen:
                seen.add(laptop_id)
                unique_laptops.append(laptop)
        
        return unique_laptops

# Global instance
llm_service = LLMService()
