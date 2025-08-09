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
import threading

class MobileNewsAgent:
    """
    Mobile-optimized news aggregation agent for Android
    """
    
    def __init__(self, callback=None):
        self.setup_logging()
        self.news_sources = [
            "http://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss", 
            "https://feeds.reuters.com/reuters/topNews",
            "https://feeds.npr.org/1001/rss.xml"
        ]
        self.articles = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NewsAgent-Mobile/1.0'
        })
        self.callback = callback  # For UI updates
        self.is_running = False
        
    def setup_logging(self):
        """Configure logging for mobile"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('MobileNewsAgent')
        
    def update_status(self, message):
        """Update UI status if callback is provided"""
        if self.callback:
            self.callback(message)
        self.logger.info(message)
        
    def plan_task(self, user_query: str) -> List[str]:
        """Plan execution steps based on query"""
        self.update_status(f"🧠 Planning task: {user_query}")
        
        plan = []
        
        if any(word in user_query.lower() for word in ['news', 'articles', 'headlines']):
            plan.extend([
                "fetch_news_feeds",
                "extract_article_content", 
                "analyze_content_quality",
                "summarize_articles",
                "rank_by_relevance",
                "generate_summary_report"
            ])
            
        if any(word in user_query.lower() for word in ['tech', 'technology', 'ai']):
            plan.append("filter_tech_content")
            
        if not plan:
            plan = ["fetch_news_feeds", "summarize_articles", "generate_summary_report"]
            
        return plan
        
    def fetch_news_feeds(self) -> Dict[str, Any]:
        """Fetch news from RSS feeds"""
        self.update_status("📡 Fetching news feeds...")
        
        all_articles = []
        successful_sources = 0
        
        for i, source_url in enumerate(self.news_sources):
            try:
                self.update_status(f"📰 Source {i+1}/{len(self.news_sources)}")
                feed = feedparser.parse(source_url)
                
                for entry in feed.entries[:5]:
                    article = {
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', ''),
                        'source': source_url,
                        'content': '',
                        'word_count': 0,
                        'readability_score': 0,
                        'relevance_score': 0,
                        'quality_score': 0
                    }
                    all_articles.append(article)
                    
                successful_sources += 1
                
            except Exception as e:
                self.logger.error(f"Failed to fetch from {source_url}: {e}")
                
        self.articles = all_articles
        
        return {
            'total_articles': len(all_articles),
            'successful_sources': successful_sources
        }
        
    def extract_article_content(self) -> Dict[str, Any]:
        """Extract content from top articles only (mobile optimization)"""
        self.update_status("📄 Extracting article content...")
        
        extracted_count = 0
        # Limit to top 5 articles for mobile performance
        for i, article in enumerate(self.articles[:5]):
            try:
                if article['link']:
                    self.update_status(f"📖 Reading article {i+1}/5")
                    response = self.session.get(article['link'], timeout=8)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract content
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
                        paragraphs = soup.find_all('p')
                        content = ' '.join([p.get_text() for p in paragraphs])
                    
                    content = re.sub(r'\s+', ' ', content).strip()
                    article['content'] = content[:1500]  # Limit for mobile
                    article['word_count'] = len(content.split())
                    
                    extracted_count += 1
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                self.logger.error(f"Failed to extract content: {e}")
                
        return {'extracted_articles': extracted_count}
        
    def analyze_content_quality(self) -> Dict[str, Any]:
        """Analyze content quality"""
        self.update_status("🔍 Analyzing content quality...")
        
        for article in self.articles:
            if article['content']:
                try:
                    article['readability_score'] = textstat.flesch_reading_ease(article['content'])
                except:
                    article['readability_score'] = 50  # Default
                
                # Quality scoring
                quality_score = 0
                if article['word_count'] > 100: quality_score += 20
                if article['word_count'] > 300: quality_score += 20
                if len(article['title']) > 10: quality_score += 10
                if article['summary']: quality_score += 10
                
                article['quality_score'] = quality_score
                
        return {'analyzed_articles': len([a for a in self.articles if a['content']])}
        
    def summarize_articles(self) -> Dict[str, Any]:
        """Generate summaries using simple text processing"""
        self.update_status("📝 Generating summaries...")
        
        summarized_count = 0
        
        for article in self.articles:
            if article['content'] and len(article['content']) > 100:
                try:
                    sentences = article['content'].split('. ')
                    summary_sentences = sentences[:2]  # Shorter for mobile
                    article['ai_summary'] = '. '.join(summary_sentences)[:150] + "..."
                    summarized_count += 1
                except Exception as e:
                    article['ai_summary'] = article['summary'][:150]
            else:
                article['ai_summary'] = article['summary'][:150] if article['summary'] else "No summary available"
                        
        return {'summarized_articles': summarized_count}
        
    def rank_by_relevance(self) -> Dict[str, Any]:
        """Rank articles by relevance"""
        self.update_status("📊 Ranking articles...")
        
        for article in self.articles:
            relevance_score = 0
            
            # Title relevance
            title_keywords = ['breaking', 'urgent', 'major', 'significant', 'important']
            if any(keyword in article['title'].lower() for keyword in title_keywords):
                relevance_score += 20
                
            relevance_score += article.get('quality_score', 0)
            
            if article.get('readability_score', 0) > 60:
                relevance_score += 10
                
            relevance_score += random.randint(0, 10)
            
            article['relevance_score'] = relevance_score
            
        self.articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {'total_ranked': len(self.articles)}
        
    def filter_tech_content(self) -> Dict[str, Any]:
        """Filter for tech content"""
        self.update_status("🔧 Filtering tech content...")
        
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
        """Generate mobile-friendly summary report"""
        self.update_status("📋 Generating report...")
        
        if not self.articles:
            return {'report': 'No articles found to summarize.'}
            
        top_articles = self.articles[:3]  # Top 3 for mobile
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_articles_processed': len(self.articles),
            'top_articles': []
        }
        
        for i, article in enumerate(top_articles, 1):
            article_summary = {
                'rank': i,
                'title': article['title'],
                'summary': article.get('ai_summary', article['summary'])[:120],
                'relevance_score': article['relevance_score'],
                'word_count': article['word_count'],
                'link': article['link']
            }
            report['top_articles'].append(article_summary)
            
        avg_score = sum(a['relevance_score'] for a in self.articles) / max(1, len(self.articles))
        report['insights'] = {
            'average_relevance_score': round(avg_score, 2),
            'content_quality': 'High' if avg_score > 30 else 'Medium' if avg_score > 15 else 'Basic'
        }
        
        return report
        
    def run_async(self, user_query: str = "Get me the latest news"):
        """Run agent asynchronously for mobile UI"""
        def run_task():
            self.is_running = True
            try:
                self.update_status("🚀 Starting news agent...")
                
                plan = self.plan_task(user_query)
                results = {}
                
                for step in plan:
                    if not self.is_running:  # Allow cancellation
                        break
                        
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
                        
                    time.sleep(0.5)  # UI breathing room
                    
                self.update_status("✅ Agent completed!")
                
                # Return results via callback
                if self.callback:
                    final_results = {
                        'query': user_query,
                        'plan': plan,
                        'execution_results': results,
                        'articles_processed': len(self.articles),
                        'completion_time': datetime.now().isoformat()
                    }
                    self.callback({'type': 'results', 'data': final_results})
                    
            except Exception as e:
                self.update_status(f"❌ Error: {str(e)}")
                if self.callback:
                    self.callback({'type': 'error', 'message': str(e)})
            finally:
                self.is_running = False
                
        thread = threading.Thread(target=run_task)
        thread.daemon = True
        thread.start()
        
    def stop(self):
        """Stop the running agent"""
        self.is_running = False
        self.update_status("🛑 Agent stopped")