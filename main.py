from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform
import threading
from mobile_agent import MobileNewsAgent

class ArticleCard(BoxLayout):
    """Widget for displaying a single article"""
    
    def __init__(self, article_data, **kwargs):
        super(ArticleCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = '120dp'
        self.spacing = '5dp'
        self.padding = ['10dp', '5dp', '10dp', '5dp']
        
        # Create a colored background
        from kivy.graphics import Color, Rectangle
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Rank badge
        rank_label = Label(
            text=f"#{article_data['rank']}",
            size_hint=(None, None),
            size=('30dp', '30dp'),
            color=(1, 1, 1, 1),
            bold=True
        )
        
        # Title
        title_label = Label(
            text=article_data['title'][:80] + "..." if len(article_data['title']) > 80 else article_data['title'],
            size_hint_y=None,
            height='30dp',
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Summary
        summary_label = Label(
            text=article_data['summary'],
            size_hint_y=None,
            height='50dp',
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.4, 0.4, 0.4, 1)
        )
        summary_label.bind(size=summary_label.setter('text_size'))
        
        # Meta info
        meta_label = Label(
            text=f"Score: {article_data['relevance_score']} | Words: {article_data['word_count']}",
            size_hint_y=None,
            height='20dp',
            color=(0.6, 0.6, 0.6, 1),
            font_size='12sp'
        )
        
        self.add_widget(rank_label)
        self.add_widget(title_label)
        self.add_widget(summary_label)
        self.add_widget(meta_label)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class NewsAgentApp(App):
    """Main mobile news agent application"""
    
    def build(self):
        self.title = "📰 News Agent"
        self.agent = MobileNewsAgent(callback=self.agent_callback)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')
        
        # Header
        header = Label(
            text="🤖 News Agent Mobile",
            size_hint_y=None,
            height='50dp',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        # Input section
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        
        self.query_input = TextInput(
            hint_text="Enter your news query (e.g., 'latest tech news')",
            multiline=False,
            size_hint_x=0.7
        )
        
        self.run_button = Button(
            text="🚀 Run",
            size_hint_x=0.3,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.run_button.bind(on_press=self.run_agent)
        
        input_layout.add_widget(self.query_input)
        input_layout.add_widget(self.run_button)
        
        # Status display
        self.status_label = Label(
            text="📱 Ready to fetch news!",
            size_hint_y=None,
            height='30dp',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # Results scroll area
        self.results_scroll = ScrollView()
        self.results_layout = GridLayout(cols=1, size_hint_y=None, spacing='5dp')
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        
        # Add widgets to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.results_scroll)
        
        return main_layout
    
    def run_agent(self, instance):
        """Start the news agent"""
        query = self.query_input.text or "Get me the latest news"
        
        # Disable button and clear results
        self.run_button.disabled = True
        self.run_button.text = "⏳ Running..."
        self.clear_results()
        
        # Start agent
        self.agent.run_async(query)
    
    def agent_callback(self, data):
        """Handle callbacks from the agent"""
        if isinstance(data, str):
            # Status update
            Clock.schedule_once(lambda dt: self.update_status(data))
        elif isinstance(data, dict):
            if data.get('type') == 'results':
                # Results received
                Clock.schedule_once(lambda dt: self.display_results(data['data']))
            elif data.get('type') == 'error':
                # Error occurred
                Clock.schedule_once(lambda dt: self.show_error(data['message']))
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.text = message
    
    def clear_results(self):
        """Clear previous results"""
        self.results_layout.clear_widgets()
    
    def display_results(self, results):
        """Display agent results"""
        self.run_button.disabled = False
        self.run_button.text = "🚀 Run"
        
        # Add summary info
        summary_text = f"📊 Processed {results['articles_processed']} articles"
        summary_label = Label(
            text=summary_text,
            size_hint_y=None,
            height='40dp',
            color=(0.2, 0.6, 0.2, 1),
            bold=True
        )
        self.results_layout.add_widget(summary_label)
        
        # Add execution plan
        plan_text = f"🗺️ Plan: {' → '.join(results['plan'])}"
        plan_label = Label(
            text=plan_text,
            size_hint_y=None,
            height='60dp',
            text_size=(None, None),
            halign='left',
            color=(0.4, 0.4, 0.4, 1)
        )
        plan_label.bind(size=plan_label.setter('text_size'))
        self.results_layout.add_widget(plan_label)
        
        # Display articles if available
        if 'generate_summary_report' in results['execution_results']:
            report = results['execution_results']['generate_summary_report']
            
            if isinstance(report, dict) and 'top_articles' in report:
                # Add section header
                articles_header = Label(
                    text="📰 Top Articles",
                    size_hint_y=None,
                    height='40dp',
                    font_size='18sp',
                    bold=True,
                    color=(0.2, 0.2, 0.8, 1)
                )
                self.results_layout.add_widget(articles_header)
                
                # Add article cards
                for article in report['top_articles']:
                    card = ArticleCard(article)
                    self.results_layout.add_widget(card)
                    
                # Add insights if available
                if 'insights' in report:
                    insights = report['insights']
                    insights_text = f"🧠 Quality: {insights['content_quality']} | Avg Score: {insights['average_relevance_score']}"
                    insights_label = Label(
                        text=insights_text,
                        size_hint_y=None,
                        height='30dp',
                        color=(0.6, 0.3, 0.8, 1)
                    )
                    self.results_layout.add_widget(insights_label)
            else:
                # Fallback: show raw data
                debug_label = Label(
                    text=f"Debug: {str(report)[:200]}...",
                    size_hint_y=None,
                    height='100dp',
                    text_size=(None, None),
                    halign='left'
                )
                debug_label.bind(size=debug_label.setter('text_size'))
                self.results_layout.add_widget(debug_label)
    
    def show_error(self, error_message):
        """Show error popup"""
        self.run_button.disabled = False
        self.run_button.text = "🚀 Run"
        
        popup = Popup(
            title='❌ Error',
            content=Label(text=f"Error: {error_message}"),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def on_pause(self):
        """Handle app pause (Android)"""
        return True
    
    def on_resume(self):
        """Handle app resume (Android)"""
        pass

if __name__ == '__main__':
    NewsAgentApp().run()