from EmotionDetection.emotion_detection import emotion_detector
import unittest

class TestEmotionDetection(unittest.TestCase):
    def test_statement(self):
        text_to_analyze = "I am really mad about this."
        result = emotion_detector(text_to_analyze)
        self.assertEqual(result['dominant_emotion'], 'anger')
        text_to_analyze = "I am glad this happened."
        result = emotion_detector(text_to_analyze)
        self.assertEqual(result['dominant_emotion'], 'joy')
        text_to_analyze = "I feel disgusted just hearing about this."
        result = emotion_detector(text_to_analyze)
        self.assertEqual(result['dominant_emotion'], 'disgust')
        text_to_analyze = "I am so sad about this."
        result = emotion_detector(text_to_analyze)
        self.assertEqual(result['dominant_emotion'], 'sadness')
        text_to_analyze = "I am really afraid that this will happen."
        result = emotion_detector(text_to_analyze)
        self.assertEqual(result['dominant_emotion'], 'fear')

if __name__ == '__main__':
    unittest.main()
