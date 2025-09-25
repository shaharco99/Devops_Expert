from playwright.sync_api import sync_playwright

def test_scores_service():
    """
    Tests the score service by navigating to the URL, retrieving the score,
    and asserting that the score is an integer.
    """
    url_score = "http://localhost:5000/"

    # Use a 'with' statement for Playwright to ensure resources are closed properly
    with sync_playwright() as p:
        # Launch a headless Chrome browser
        browser = p.chromium.launch(headless=True)
        # Create a new page (tab)
        page = browser.new_page()
        # Navigate to the specified URL
        page.goto(url_score)

        try:
            # Find the element with the ID "score" and get its text content
            score_text = page.inner_text("#score")
            # Convert the text to an integer
            score = int(score_text)
            # Assert that the score is an integer
            assert isinstance(score, int)
            print(f"Test passed: The score '{score}' is an integer.")
        except ValueError:
            # Handle the case where the text cannot be converted to an integer
            print("Test failed: The score is not a valid integer.")
            assert False
        finally:
            # Close the browser
            browser.close()

# Run the test function
test_scores_service()