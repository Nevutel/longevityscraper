import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import logging

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class FreeSummarizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\,]', '', text)
        return text
    
    def extractive_summarize(self, text, max_sentences=3):
        """Simple extractive summarization - takes first few sentences"""
        if not text or len(text) < 100:
            return text
        
        # Clean the text
        text = self.clean_text(text)
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Take the first few sentences
        summary_sentences = sentences[:max_sentences]
        summary = ' '.join(summary_sentences)
        
        # Add ellipsis if we truncated
        if len(sentences) > max_sentences:
            summary += "..."
        
        return summary
    
    def tfidf_summarize(self, text, max_sentences=3):
        """TF-IDF based summarization - finds most important sentences"""
        if not text or len(text) < 100:
            return text
        
        # Clean the text
        text = self.clean_text(text)
        
        # Split into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Create TF-IDF vectorizer
        try:
            vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 2),
                max_features=1000
            )
            
            # Create TF-IDF matrix
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Calculate sentence scores based on TF-IDF values
            sentence_scores = []
            for i in range(len(sentences)):
                score = np.mean(tfidf_matrix[i].toarray())
                sentence_scores.append((score, i))
            
            # Sort sentences by score and take top ones
            sentence_scores.sort(reverse=True)
            top_indices = [idx for score, idx in sentence_scores[:max_sentences]]
            top_indices.sort()  # Keep original order
            
            # Create summary
            summary_sentences = [sentences[i] for i in top_indices]
            summary = ' '.join(summary_sentences)
            
            return summary
            
        except Exception as e:
            self.logger.error(f"TF-IDF summarization failed: {str(e)}")
            # Fallback to extractive summarization
            return self.extractive_summarize(text, max_sentences)
    
    def keyword_based_summarize(self, text, max_sentences=3):
        """Keyword-based summarization using anti-aging related keywords"""
        if not text or len(text) < 100:
            return text
        
        # Anti-aging related keywords (weighted)
        keywords = {
            'anti-aging': 3, 'longevity': 3, 'senescence': 3, 'aging': 2,
            'telomere': 3, 'sirtuin': 3, 'rapamycin': 3, 'metformin': 3,
            'NAD+': 3, 'mitochondria': 2, 'autophagy': 3, 'inflammation': 2,
            'oxidative stress': 3, 'cellular aging': 3, 'biological age': 3,
            'epigenetic clock': 3, 'senolytics': 3, 'gerontology': 2,
            'research': 1, 'study': 1, 'clinical': 1, 'trial': 1
        }
        
        # Clean the text
        text = self.clean_text(text)
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences based on keyword presence
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()
            
            for keyword, weight in keywords.items():
                if keyword.lower() in sentence_lower:
                    score += weight
            
            sentence_scores.append((score, i))
        
        # Sort by score and take top sentences
        sentence_scores.sort(reverse=True)
        top_indices = [idx for score, idx in sentence_scores[:max_sentences]]
        top_indices.sort()  # Keep original order
        
        summary_sentences = [sentences[i] for i in top_indices]
        summary = ' '.join(summary_sentences)
        
        return summary
    
    def summarize(self, text, method='hybrid', max_sentences=3):
        """Main summarization method with multiple options"""
        if not text or len(text) < 100:
            return text
        
        try:
            if method == 'extractive':
                return self.extractive_summarize(text, max_sentences)
            elif method == 'tfidf':
                return self.tfidf_summarize(text, max_sentences)
            elif method == 'keyword':
                return self.keyword_based_summarize(text, max_sentences)
            elif method == 'hybrid':
                # Try TF-IDF first, fallback to keyword-based, then extractive
                try:
                    return self.tfidf_summarize(text, max_sentences)
                except:
                    try:
                        return self.keyword_based_summarize(text, max_sentences)
                    except:
                        return self.extractive_summarize(text, max_sentences)
            else:
                return self.extractive_summarize(text, max_sentences)
                
        except Exception as e:
            self.logger.error(f"Summarization failed: {str(e)}")
            return text[:500] + "..." if len(text) > 500 else text 