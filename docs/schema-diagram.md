# Schema Diagram

## Dataset Architecture

```mermaid
erDiagram
    LAPTOP_INFO {
        string Brand "Primary Brand"
        string Model "Model Name"
        string Price_Details "Pricing Information (String)"
        string Availability "Stock Status (String)"
        string Promos_Offers "Promotional Offers (String)"
        string Review_Details "Review Data (String/Generated)"
        string QA_FAQ "Questions & Answers (String/Generated)"
        string Processor "CPU Specifications"
        string Operating_System "OS Information"
        string Graphics "GPU Details"
        string Chipset "Chipset Information"
        string Memory_RAM "RAM Specifications"
        string Storage "Storage Details"
        string Display "Screen Specifications"
        string External_Monitor_Support "Display Support"
        string Audio "Audio System"
        string Camera "Webcam Details"
        string Input_Devices "Keyboard & Pointing"
        string Dimensions_Weight "Physical Specs"
        string Case_Chassis "Build Materials"
        string Ports "Connectivity"
        string Card_Reader "Memory Card Reader"
        string Wireless_Networking "WiFi & Bluetooth"
        string Wired_Networking "Ethernet"
        string Mobile_Broadband "Cellular"
        string Docking "Docking Support"
        string Battery "Battery Specs"
        string Power_Adapter "Charger Details"
        string Biometric_Security "Fingerprint Reader"
        string General_Security "Security Features"
        string Software_Management "Pre-installed Software"
        string Warranty "Warranty Information"
        string Environmental_Durability "Certifications"
    }
```

## Data Flow Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        A[HP PDF Specs] --> E[Data Integration]
        B[Other Brand PDFs] --> E
        C[Marketplace Data] --> E
        D[Review Data] --> E
    end
    
    subgraph "Processing Layer"
        E --> F[Data Cleaning]
        F --> G[Schema Mapping]
        G --> H[Data Validation]
        H --> I[Data Generation]
    end
    
    subgraph "Storage Layer"
        I --> J[laptop_info_cleaned.csv]
    end
    
    subgraph "API Layer"
        J --> K[Data Service]
        K --> L[Explore API]
        K --> M[Search API]
        K --> N[Reviews API]
        K --> O[Recommendations API]
        K --> P[Chat API]
    end
    
    subgraph "AI Layer"
        Q[DeepSeek API] --> P
        Q --> O
    end
    
    subgraph "Frontend Layer"
        L --> R[Explore & Compare]
        M --> R
        N --> S[Reviews Intelligence]
        P --> T[Chat & Recommend]
        O --> T
    end
```

## API Endpoint Structure

```mermaid
graph LR
    subgraph "API v1"
        A["/api/v1/health"] --> B[Health Check]
        C["/api/v1/info"] --> D[API Information]
        
        subgraph "Explore Endpoints"
            E["/api/v1/explore/"] --> F[Get All Laptops]
            G["/api/v1/explore/{id}"] --> H[Get Laptop by ID]
            I["/api/v1/explore/filter-options"] --> J[Get Filter Options]
            K["/api/v1/explore/price-trends"] --> L[Get Price Trends]
            M["/api/v1/explore/availability"] --> N[Get Availability]
            O["/api/v1/explore/search"] --> P[Search Laptops]
            Q["/api/v1/explore/{id}/specifications"] --> R[Get Specifications]
        end
        
        subgraph "Reviews Endpoints"
            S["/api/v1/reviews/"] --> T[Get Review Stats]
            U["/api/v1/reviews/volume-trends"] --> V[Get Volume Trends]
            W["/api/v1/reviews/rating-trends"] --> X[Get Rating Trends]
            Y["/api/v1/reviews/top-themes"] --> Z[Get Top Themes]
            AA["/api/v1/reviews/top-attributes"] --> BB[Get Top Attributes]
            CC["/api/v1/reviews/rating-distribution"] --> DD[Get Rating Distribution]
            EE["/api/v1/reviews/brand-comparison"] --> FF[Get Brand Comparison]
        end
        
        subgraph "Recommendations Endpoints"
            GG["/api/v1/recommendations/constraint-based"] --> HH[Get Constraint Recommendations]
            II["/api/v1/recommendations/similar/{id}"] --> JJ[Get Similar Laptops]
            KK["/api/v1/recommendations/trending"] --> LL[Get Trending Laptops]
            MM["/api/v1/recommendations/budget/{price}"] --> NN[Get Budget Recommendations]
            OO["/api/v1/recommendations/brand/{brand}"] --> PP[Get Brand Recommendations]
            QQ["/api/v1/recommendations/use-case"] --> RR[Get Use Case Recommendations]
        end
        
        subgraph "Chat Endpoints"
            SS["/api/v1/chat/query"] --> TT[Chat Query]
            UU["/api/v1/chat/recommend"] --> VV[Get AI Recommendations]
            WW["/api/v1/chat/compare"] --> XX[Compare Laptops]
        end
    end
```

## Frontend Component Structure

```mermaid
graph TB
    subgraph "React Application"
        A[App.js] --> B[ChatRecommend]
        
        subgraph "Chat & Recommend Components"
            B --> C[Chat Interface]
            B --> D[Recommendation Form]
            B --> E[AI Responses]
            B --> F[Constraint Builder]
            B --> G[Explore Tab]
            B --> H[Reviews Tab]
        end
        
        subgraph "Explore & Compare Components"
            G --> I[Search Bar]
            G --> J[Filter Panel]
            G --> K[Laptop Grid]
            G --> L[Comparison Modal]
            G --> M[Price Trends]
            G --> N[Availability Chart]
        end
        
        subgraph "Reviews Intelligence Components"
            H --> O[Rating Charts]
            H --> P[Theme Analysis]
            H --> Q[Top Rated List]
            H --> R[Review Statistics]
            H --> S[Brand Comparison]
            H --> T[Rating Distribution]
        end
        
        subgraph "Shared Services"
            U[API Service] --> V[HTTP Client]
            U --> W[Error Handling]
            U --> X[Data Transformation]
        end
        
        B --> U
        G --> U
        H --> U
    end
```

## Data Processing Pipeline

```mermaid
flowchart TD
    subgraph "Data Ingestion"
        A[PDF Specifications] --> E[Text Extraction]
        B[Marketplace Scraping] --> F[HTML Parsing]
        C[Review Scraping] --> G[Sentiment Analysis]
        D[Price Monitoring] --> H[Price Extraction]
    end
    
    subgraph "Data Processing"
        E --> I[Data Cleaning]
        F --> I
        G --> I
        H --> I
        
        I --> J[Schema Mapping]
        J --> K[Data Validation]
        K --> L[Data Enrichment]
        L --> M[Data Generation]
    end
    
    subgraph "Data Storage"
        M --> N[laptop_info_cleaned.csv]
        N --> O[Data Service Layer]
    end
    
    subgraph "API Processing"
        O --> P[Request Handling]
        P --> Q[Data Filtering]
        Q --> R[Response Formatting]
        R --> S[JSON Response]
    end
    
    subgraph "AI Processing"
        T[DeepSeek API] --> U[Query Processing]
        U --> V[Context Building]
        V --> W[Response Generation]
        W --> X[Citation Extraction]
    end
    
    subgraph "Frontend Processing"
        S --> Y[Data Fetching]
        Y --> Z[State Management]
        Z --> AA[Component Rendering]
        X --> Y
    end
```

## System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser] --> B[React Frontend]
        B --> C[API Client]
    end
    
    subgraph "Application Layer"
        C --> D[FastAPI Backend]
        D --> E[API Endpoints]
        E --> F[Business Logic]
    end
    
    subgraph "Data Layer"
        F --> G[Data Service]
        G --> H[CSV Data Source]
        F --> I[LLM Service]
        I --> J[DeepSeek API]
        F --> K[Recommendation Service]
    end
    
    subgraph "External Services"
        J --> L[DeepSeek Platform]
        H --> M[File System]
    end
    
    subgraph "Infrastructure"
        N[Docker Containers] --> O[Backend Container]
        N --> P[Frontend Container]
        Q[Load Balancer] --> R[Production Servers]
    end
```

This schema diagram provides a comprehensive overview of the Laptop Assistant platform architecture, including:

1. **Dataset Structure**: Entity-relationship diagram showing the main data fields
2. **Data Flow**: How data moves from sources to the frontend
3. **API Structure**: Complete endpoint hierarchy with correct paths
4. **Frontend Components**: React component organization with tabbed interface
5. **Processing Pipeline**: Data transformation workflow including generation
6. **System Architecture**: Overall system design with FastAPI backend

The diagrams use Mermaid syntax and can be rendered in GitHub, GitLab, or other Markdown viewers that support Mermaid diagrams.



