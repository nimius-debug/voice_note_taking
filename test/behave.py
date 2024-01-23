from unittest.mock import AsyncMock, patch
import unittest
from transcription import transcribe_live

class TestTranscription(unittest.TestCase):
    @patch('transcription.DeepgramClient')
    @patch('transcription.Microphone')
    def test_transcribe_live(self, MockMic, MockDGClient):
        # Mock the Deepgram client and microphone
        MockDGClient.listen.live.v.return_value = AsyncMock()
        MockMic.return_value = AsyncMock()

        # Mock the session state
        session_state = {'state': True, 'transcription': ''}

        # Run transcribe_live (consider running in an event loop)
        # transcribe_live(...)

        # Assertions here
        pass

if __name__ == '__main__':
    unittest.main()