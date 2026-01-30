"""
Updated Streamlit Dashboard for DevUnfiltered Bot
Displays engagement metrics, post history, and bot status
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Page configuration
st.set_page_config(
    page_title="DevUnfiltered Bot Dashboard",
    page_icon="🔥",
    layout="wide"
)

# File paths
ACTIVITY_LOG = 'bot_activity.json'
POSTED_HISTORY = 'posted_history.json'
TOPIC_HISTORY = 'topic_history.json'


def load_json_file(filepath, default=None):
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else {}
    except json.JSONDecodeError:
        st.error(f"Error reading {filepath} - invalid JSON")
        return default if default is not None else {}


def format_time_ago(iso_timestamp):
    """Format ISO timestamp as 'X hours/days ago'"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    except:
        return "Unknown"


def main():
    st.title("🔥 DevUnfiltered Bot Dashboard")
    st.markdown("*Unfiltered tech takes that start arguments*")
    
    # Load data
    activity = load_json_file(ACTIVITY_LOG, default={
        'total_posts': 0,
        'successful_posts': 0,
        'failed_posts': 0,
        'total_rejections': 0,
        'last_post_time': None,
        'next_post_time': None
    })
    
    history = load_json_file(POSTED_HISTORY, default=[])
    topic_history = load_json_file(TOPIC_HISTORY, default={'topics': []})
    
    # Sidebar - Bot Status
    with st.sidebar:
        st.header("🤖 Bot Status")
        
        if activity.get('last_post_time'):
            last_post = format_time_ago(activity['last_post_time'])
            st.success(f"✅ Last post: {last_post}")
        else:
            st.info("No posts yet")
        
        if activity.get('next_post_time'):
            next_post_dt = datetime.fromisoformat(activity['next_post_time'])
            now = datetime.now()
            
            if next_post_dt > now:
                diff = next_post_dt - now
                hours = diff.seconds // 3600
                minutes = (diff.seconds % 3600) // 60
                st.info(f"⏱️ Next post in: {hours}h {minutes}m")
            else:
                st.warning("⚠️ Post overdue")
        
        st.markdown("---")
        
        # Quick stats
        st.metric("Total Posts", activity.get('total_posts', 0))
        st.metric("Success Rate", 
                 f"{(activity.get('successful_posts', 0) / max(activity.get('total_posts', 1), 1) * 100):.1f}%")
        st.metric("Total Rejections", activity.get('total_rejections', 0))
    
    # Main content - Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📝 Recent Posts", "❌ Rejections", "🔥 Topics"])
    
    # Tab 1: Overview
    with tab1:
        st.header("Engagement Metrics")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Successful Posts",
                activity.get('successful_posts', 0),
                delta=None
            )
        
        with col2:
            st.metric(
                "Failed Posts",
                activity.get('failed_posts', 0),
                delta=None
            )
        
        with col3:
            # Count content types
            controversial_count = sum(1 for p in history if p.get('content_type') == 'controversial')
            st.metric(
                "Controversial",
                controversial_count
            )
        
        with col4:
            relatable_count = sum(1 for p in history if p.get('content_type') == 'relatable')
            st.metric(
                "Relatable",
                relatable_count
            )
        
        # Charts
        if len(history) > 0:
            st.subheader("Performance Over Time")
            
            # Prepare data for charts
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['timestamp'].dt.date
            
            # Posts per day chart
            posts_per_day = df.groupby('date').size().reset_index(name='posts')
            
            fig_posts = px.line(
                posts_per_day,
                x='date',
                y='posts',
                title='Posts Per Day',
                markers=True
            )
            fig_posts.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Posts",
                hovermode='x unified'
            )
            st.plotly_chart(fig_posts, use_container_width=True)
            
            # Content type distribution
            col1, col2 = st.columns(2)
            
            with col1:
                content_dist = df['content_type'].value_counts()
                fig_pie = px.pie(
                    values=content_dist.values,
                    names=content_dist.index,
                    title='Content Type Distribution'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Score distribution
                if 'score' in df.columns:
                    fig_scores = px.histogram(
                        df,
                        x='score',
                        nbins=10,
                        title='Score Distribution',
                        labels={'score': 'Quality Score', 'count': 'Number of Posts'}
                    )
                    st.plotly_chart(fig_scores, use_container_width=True)
        else:
            st.info("No posts yet. Start the bot to see metrics!")
    
    # Tab 2: Recent Posts
    with tab2:
        st.header("Recent Posts")
        
        if len(history) > 0:
            # Show last 20 posts
            for post in reversed(history[-20:]):
                with st.expander(
                    f"{post.get('timestamp', 'Unknown')} - "
                    f"{post.get('content_type', 'unknown').title()} - "
                    f"Score: {post.get('score', 'N/A')}/10"
                ):
                    st.markdown(f"**Content:**")
                    st.info(post.get('post_text', 'No content'))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Type:** {post.get('content_type', 'unknown')}")
                        st.markdown(f"**Score:** {post.get('score', 'N/A')}/10")
                    
                    with col2:
                        if post.get('url'):
                            st.markdown(f"**URL:** [{post['url']}]({post['url']})")
                        st.markdown(f"**Time:** {format_time_ago(post.get('timestamp', ''))}")
                    
                    if post.get('feedback'):
                        st.markdown("**Feedback:**")
                        st.text(post['feedback'])
        else:
            st.info("No posts yet. The bot will display posts here once they're published.")
    
    # Tab 3: Rejections
    with tab3:
        st.header("Rejected Posts")
        
        rejections = activity.get('rejections', [])
        
        if len(rejections) > 0:
            st.markdown(f"**Total Rejections:** {len(rejections)}")
            
            # Show rejection reasons
            st.subheader("Recent Rejections")
            
            for rejection in reversed(rejections[-10:]):
                with st.expander(
                    f"{rejection.get('timestamp', 'Unknown')} - "
                    f"{rejection.get('content_type', 'unknown').title()} - "
                    f"Score: {rejection.get('score', 'N/A')}/10"
                ):
                    st.markdown(f"**Content:**")
                    st.warning(rejection.get('post_text', 'No content'))
                    
                    st.markdown(f"**Score:** {rejection.get('score', 'N/A')}/10")
                    st.markdown(f"**Type:** {rejection.get('content_type', 'unknown')}")
                    
                    if rejection.get('feedback'):
                        st.markdown("**Feedback:**")
                        st.text(rejection['feedback'])
        else:
            st.info("No rejections yet - all generated posts have been approved!")
    
    # Tab 4: Topics
    with tab4:
        st.header("Topic Analytics")
        
        topics = topic_history.get('topics', [])
        
        if len(topics) > 0:
            st.markdown(f"**Total Topics Used:** {len(topics)}")
            
            # Count topic usage
            topic_counts = {}
            for entry in topics:
                if 'topic' in entry:
                    topic = entry['topic']
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            # Sort by usage
            sorted_topics = sorted(
                topic_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Most used topics chart
            if len(sorted_topics) > 0:
                st.subheader("Most Used Topics")
                
                top_topics = sorted_topics[:10]
                topic_df = pd.DataFrame(top_topics, columns=['Topic', 'Count'])
                
                fig_topics = px.bar(
                    topic_df,
                    x='Count',
                    y='Topic',
                    orientation='h',
                    title='Top 10 Most Used Topics'
                )
                fig_topics.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_topics, use_container_width=True)
            
            # Recent topics
            st.subheader("Recent Topics")
            recent_topics = [t.get('topic', 'Unknown') for t in reversed(topics[-10:])]
            for i, topic in enumerate(recent_topics, 1):
                st.text(f"{i}. {topic}")
        else:
            st.info("No topics tracked yet. Topics will appear here as posts are made.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "*Dashboard updates in real-time as the bot posts. "
        "Refresh the page to see latest data.*"
    )


if __name__ == "__main__":
    main()
