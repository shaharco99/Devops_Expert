from requests import get
import re

def test_scores_service():
    url_score = "http://score:5000/"  # service name in docker-compose
    resp = get(url_score, timeout=10)
    resp.raise_for_status()
    m = re.search(r'id="score">(\d+)<', resp.text)
    assert m is not None, "score element not found in page"
    score = int(m.group(1))
    assert isinstance(score, int)

# Run the test function
if __name__ == '__main__':
    test_scores_service()