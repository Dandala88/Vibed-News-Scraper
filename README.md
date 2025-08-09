# 🤖 News Aggregation Agent

An intelligent agent that demonstrates autonomous task planning, web scraping, content analysis, and AI-powered summarization.

## 🚀 What This Agent Does

This agent showcases key AI agent principles:

1. **Autonomous Planning** - Breaks down user queries into actionable steps
2. **Web Scraping** - Gathers news from multiple RSS sources  
3. **Content Analysis** - Evaluates article quality and readability
4. **AI Summarization** - Uses transformer models to generate summaries
5. **Decision Making** - Ranks content by relevance and quality
6. **User Interface** - Provides a beautiful web dashboard

## 🏗️ Agent Architecture

```
NewsAgent
├── Task Planning (plan_task)
├── Execution Engine (execute_plan)
├── Data Collection (fetch_news_feeds)
├── Content Processing (extract_article_content)
├── AI Analysis (summarize_articles, analyze_content_quality)
├── Decision Making (rank_by_relevance)
└── Reporting (generate_summary_report)
```

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the agent directly:
```bash
python agent.py
```

3. Or start the web interface:
```bash
python web_interface.py
```

Then visit http://localhost:5000

## 🎯 Key Agent Features

### Autonomous Planning
The agent analyzes user queries and creates execution plans:
```python
plan = agent.plan_task("Get me tech news and summarize it")
# Result: ["fetch_news_feeds", "filter_tech_content", "summarize_articles", "generate_summary_report"]
```

### Multi-Source Data Collection
Fetches from multiple news sources:
- BBC News RSS
- CNN RSS  
- Reuters RSS
- NPR RSS

### AI-Powered Analysis
- **Content Extraction**: Intelligently extracts article text
- **Quality Analysis**: Evaluates readability and content quality
- **AI Summarization**: Uses BART model for article summaries
- **Relevance Ranking**: Scores articles by importance and quality

### Error Handling & Logging
- Comprehensive logging system
- Graceful error handling
- Rate limiting for web requests
- Fallback mechanisms

## 🌟 Example Usage

### Command Line
```python
from agent import NewsAgent

agent = NewsAgent()
results = agent.run("Get me the latest tech news and summarize the top stories")

print(f"Processed {results['articles_processed']} articles")
print(f"Plan: {results['plan']}")
```

### Web Interface
1. Start the web server: `python web_interface.py`
2. Open http://localhost:5000
3. Enter your query (e.g., "Get me breaking news about AI")
4. Watch the agent work autonomously
5. View the ranked and summarized results

## 🧠 Agent Learning Concepts

This project demonstrates:

### 1. Task Decomposition
The agent breaks complex requests into manageable subtasks

### 2. Autonomous Execution  
Once planned, the agent executes tasks without human intervention

### 3. Multi-Modal Processing
Combines web scraping, NLP, and machine learning

### 4. Adaptive Behavior
Adjusts behavior based on content type and user queries

### 5. State Management
Maintains context throughout the execution pipeline

### 6. Error Recovery
Gracefully handles failures and provides fallback options

## 🔧 Customization

### Adding News Sources
```python
self.news_sources = [
    "your_rss_feed_url_here",
    # ... existing sources
]
```

### Custom Filters
```python
def filter_custom_content(self):
    keywords = ['your', 'custom', 'keywords']
    # Filter logic here
```

### Different AI Models
```python
self.summarizer = pipeline("summarization", model="your-preferred-model")
```

## 📊 Agent Performance

The agent processes:
- ✅ Multiple RSS feeds simultaneously
- ✅ Content extraction from full articles  
- ✅ AI-powered summarization
- ✅ Quality scoring and ranking
- ✅ Real-time progress tracking

## 🎓 Learning Outcomes

After studying this agent, you'll understand:

1. **Agent Architecture** - How to structure autonomous agents
2. **Task Planning** - Breaking down complex goals
3. **Web Scraping** - Ethical data collection techniques
4. **NLP Integration** - Using transformer models in agents
5. **User Interfaces** - Building agent interaction systems
6. **Error Handling** - Building robust autonomous systems

## 🚦 Running the Agent

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run web interface
python web_interface.py

# Visit http://localhost:5000
```

### Command Line Usage
```bash
python agent.py
```

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new news sources
- Implement different AI models
- Enhance the planning algorithms
- Improve the web interface
- Add new analysis features

## 📄 License

This project is for educational purposes. Be mindful of:
- RSS feed usage policies
- Rate limiting for web scraping
- AI model licensing
- Data privacy considerations

---

**Happy Agent Building! 🤖✨**