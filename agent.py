import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import time
import random
from typing import List, Dict, Any
import json
import re
import textstat
# Removed transformers dependency for easier setup

class NewsAgent:
    """
    An intelligent news aggregation agent that:
    1. Plans its own tasks
    2. Scrapes news from multiple sources
    3. Processes and summarizes content
    4. Makes decisions about content relevance
    """
    
    def __init__(self):
        self.setup_logging()
        self.news_sources = [
            "http://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss",
            "https://feeds.reuters.com/reuters/topNews",
            "https://feeds.npr.org/1001/rss.xml"
        ]
        self.articles = []
        self.summarizer = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def setup_logging(self):
        """Configure logging for the agent"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('NewsAgent')
        
    def plan_task(self, user_query: str) -> List[str]:
        """
        Agent planning: Break down the user's request into actionable steps
        This demonstrates autonomous task planning
        """
        self.logger.info(f"Planning task for query: {user_query}")
        
        # Simple keyword-based planning (in a real agent, this could use LLM planning)
        plan = []
        
        if any(word in user_query.lower() for word in ['news', 'articles', 'headlines']):
            plan.extend([
                "fetch_news_feeds",
                "extract_article_content", 
                "analyze_content_quality",
                "summarize_articles",
                "rank_by_relevance",
                "generate_summary_report"  # Always generate report for news queries
            ])
            
        if any(word in user_query.lower() for word in ['tech', 'technology', 'ai']):
            plan.append("filter_tech_content")
            
        if not plan:
            plan = ["fetch_news_feeds", "summarize_articles", "generate_summary_report"]
            
        self.logger.info(f"Generated plan: {plan}")
        return plan
        
    def execute_plan(self, plan: List[str]) -> Dict[str, Any]:
        """Execute the planned tasks autonomously"""
        results = {}
        
        for step in plan:
            self.logger.info(f"Executing step: {step}")
            
            try:
                if step == "fetch_news_feeds":
                    results[step] = self.fetch_news_feeds()
                elif step == "extract_article_content":
                    results[step] = self.extract_article_content()
                elif step == "analyze_content_quality":
                    results[step] = self.analyze_content_quality()
                elif step == "summarize_articles":
                    results[step] = self.summarize_articles()
                elif step == "rank_by_relevance":
                    results[step] = self.rank_by_relevance()
                elif step == "generate_summary_report":
                    results[step] = self.generate_summary_report()
                elif step == "filter_tech_content":
                    results[step] = self.filter_tech_content()
                    
                # Simulate thinking time
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                self.logger.error(f"Error in step {step}: {e}")
                results[step] = f"Error: {e}"
                
        return results
        
    def fetch_news_feeds(self) -> Dict[str, Any]:
        """Fetch news from multiple RSS feeds"""
        self.logger.info("Fetching news feeds...")
        
        all_articles = []
        successful_sources = 0
        
        for source_url in self.news_sources:
            try:
                self.logger.info(f"Fetching from {source_url}")
                feed = feedparser.parse(source_url)
                
                for entry in feed.entries[:5]:  # Limit to 5 articles per source
                    article = {
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'source': source_url,
                        'content': '',
                        'word_count': 0,
                        'readability_score': 0,
                        'relevance_score': 0
                    }
                    all_articles.append(article)
                    
                successful_sources += 1
                
            except Exception as e:
                self.logger.error(f"Failed to fetch from {source_url}: {e}")
                
        self.articles = all_articles
        self.logger.info(f"Fetched {len(all_articles)} articles from {successful_sources} sources")
        
        return {
            'total_articles': len(all_articles),
            'successful_sources': successful_sources,
            'failed_sources': len(self.news_sources) - successful_sources
        }
        
    def extract_article_content(self) -> Dict[str, Any]:
        """Extract full content from article links"""
        self.logger.info("Extracting article content...")
        
        extracted_count = 0
        
        for article in self.articles[:10]:  # Limit to avoid overwhelming requests
            try:
                if article['link']:
                    response = self.session.get(article['link'], timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try to find article content
                    content_selectors = [
                        'article', '[role="main"]', '.article-body', 
                        '.story-body', '.entry-content', 'main'
                    ]
                    
                    content = ""
                    for selector in content_selectors:
                        elements = soup.select(selector)
                        if elements:
                            content = ' '.join([elem.get_text() for elem in elements])
                            break
                    
                    if not content:
                        # Fallback to paragraph tags
                        paragraphs = soup.find_all('p')
                        content = ' '.join([p.get_text() for p in paragraphs])
                    
                    # Clean up content
                    content = re.sub(r'\s+', ' ', content).strip()
                    article['content'] = content[:2000]  # Limit content length
                    article['word_count'] = len(content.split())
                    
                    extracted_count += 1
                    
                    # Rate limiting
                    time.sleep(random.uniform(1, 2))
                    
            except Exception as e:
                self.logger.error(f"Failed to extract content from {article['link']}: {e}")
                
        self.logger.info(f"Extracted content from {extracted_count} articles")
        return {'extracted_articles': extracted_count}
        
    def analyze_content_quality(self) -> Dict[str, Any]:
        """Analyze readability and quality of articles"""
        self.logger.info("Analyzing content quality...")
        
        for article in self.articles:
            if article['content']:
                # Calculate readability score
                article['readability_score'] = textstat.flesch_reading_ease(article['content'])
                
                # Simple quality indicators
                quality_score = 0
                if article['word_count'] > 100:
                    quality_score += 20
                if article['word_count'] > 300:
                    quality_score += 20
                if len(article['title']) > 10:
                    quality_score += 10
                if article['summary']:
                    quality_score += 10
                    
                article['quality_score'] = quality_score
                
        avg_readability = sum(a['readability_score'] for a in self.articles if a['readability_score']) / max(1, len([a for a in self.articles if a['readability_score']]))
        
        return {
            'analyzed_articles': len([a for a in self.articles if a['content']]),
            'average_readability': round(avg_readability, 2)
        }
        
    def summarize_articles(self) -> Dict[str, Any]:
        """Generate summaries for articles using simple text processing"""
        self.logger.info("Summarizing articles...")
        
        summarized_count = 0
        
        for article in self.articles:
            if article['content'] and len(article['content']) > 100:
                try:
                    # Simple extractive summarization - take first few sentences
                    sentences = article['content'].split('. ')
                    # Take first 2-3 sentences for summary
                    summary_sentences = sentences[:3]
                    article['ai_summary'] = '. '.join(summary_sentences)[:200] + "..."
                    summarized_count += 1
                    
                except Exception as e:
                    self.logger.error(f"Failed to summarize article: {e}")
                    article['ai_summary'] = article['summary'][:200]  # Fallback to RSS summary
            else:
                # Use RSS summary if no content
                article['ai_summary'] = article['summary'][:200] if article['summary'] else "No summary available"
                        
        return {'summarized_articles': summarized_count}
            
    def rank_by_relevance(self) -> Dict[str, Any]:
        """Rank articles by relevance and quality"""
        self.logger.info("Ranking articles by relevance...")
        
        for article in self.articles:
            relevance_score = 0
            
            # Title relevance
            title_keywords = ['breaking', 'urgent', 'major', 'significant', 'important']
            if any(keyword in article['title'].lower() for keyword in title_keywords):
                relevance_score += 20
                
            # Content quality
            relevance_score += article.get('quality_score', 0)
            
            # Readability bonus
            if article.get('readability_score', 0) > 60:  # Good readability
                relevance_score += 10
                
            # Recency bonus (if we can parse date)
            relevance_score += random.randint(0, 10)  # Simulate recency scoring
            
            article['relevance_score'] = relevance_score
            
        # Sort articles by relevance
        self.articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'total_ranked': len(self.articles),
            'top_score': self.articles[0]['relevance_score'] if self.articles else 0
        }
        
    def filter_tech_content(self) -> Dict[str, Any]:
        """Filter for technology-related content"""
        self.logger.info("Filtering for tech content...")
        
        tech_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'technology', 
            'software', 'computer', 'digital', 'tech', 'innovation', 'startup'
        ]
        
        tech_articles = []
        for article in self.articles:
            content_text = (article['title'] + ' ' + article['summary'] + ' ' + article['content']).lower()
            if any(keyword in content_text for keyword in tech_keywords):
                tech_articles.append(article)
                
        self.articles = tech_articles
        
        return {'tech_articles_found': len(tech_articles)}
        
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive summary report"""
        self.logger.info("Generating summary report...")
        
        if not self.articles:
            return {'report': 'No articles found to summarize.'}
            
        # Get top 5 articles
        top_articles = self.articles[:5]
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_articles_processed': len(self.articles),
            'top_articles': []
        }
        
        for i, article in enumerate(top_articles, 1):
            article_summary = {
                'rank': i,
                'title': article['title'],
                'summary': article.get('ai_summary', article['summary'])[:200],
                'relevance_score': article['relevance_score'],
                'word_count': article['word_count'],
                'link': article['link']
            }
            report['top_articles'].append(article_summary)
            
        # Generate insights
        avg_score = sum(a['relevance_score'] for a in self.articles) / len(self.articles)
        report['insights'] = {
            'average_relevance_score': round(avg_score, 2),
            'most_common_topics': self._extract_common_topics(),
            'content_quality': 'High' if avg_score > 30 else 'Medium' if avg_score > 15 else 'Basic'
        }
        
        return report
        
    def _extract_common_topics(self) -> List[str]:
        """Extract common topics from articles"""
        word_freq = {}
        
        for article in self.articles:
            words = article['title'].lower().split()
            for word in words:
                if len(word) > 4:  # Filter short words
                    word_freq[word] = word_freq.get(word, 0) + 1
                    
        # Return top 5 most common words
        return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
    def run(self, user_query: str = "Get me the latest news and summarize it") -> Dict[str, Any]:
        """Main agent execution method"""
        self.logger.info(f"Agent starting with query: {user_query}")
        
        # Step 1: Plan the task
        plan = self.plan_task(user_query)
        
        # Step 2: Execute the plan
        execution_results = self.execute_plan(plan)
        
        # Step 3: Return comprehensive results
        return {
            'query': user_query,
            'plan': plan,
            'execution_results': execution_results,
            'articles_processed': len(self.articles),
            'completion_time': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Example usage
    agent = NewsAgent()
    results = agent.run("Get me the latest tech news and summarize the top stories")
    
    print("\n=== AGENT EXECUTION COMPLETE ===")
    print(f"Processed {results['articles_processed']} articles")
    print(f"Execution plan: {results['plan']}")
    
    # Display top articles if available
    if 'generate_summary_report' in results['execution_results']:
        report = results['execution_results']['generate_summary_report']
        if isinstance(report, dict) and 'top_articles' in report:
            print("\n=== TOP ARTICLES ===")
            for article in report['top_articles'][:3]:
                print(f"\n{article['rank']}. {article['title']}")
                print(f"   Score: {article['relevance_score']}")
                print(f"   Summary: {article['summary']}")