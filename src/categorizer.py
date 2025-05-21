import re

PREDEFINED_CATEGORIES = [
    "Theses & Dissertations",
    "Coursework & Term Papers",
    "Certificates & Diplomas",
    "Tests & Quizzes",
    "Answer Keys & Solutions",
    "Presentations",
    "Formal Documents & Correspondence",
    "Books & Textbooks",
    "Learning Materials & Study Guides",
    "Reports"
]

class LLMCategorizer:
    def __init__(self, api_key: str = None, config: dict = None):
        """
        Initializes the LLMCategorizer.
        api_key and config are placeholders for future real LLM integration.
        """
        self.api_key = api_key
        self.config = config
        # Mock keywords for each category (case-insensitive)
        # This is a very basic placeholder.
        self._category_keywords = {
            "Theses & Dissertations": [r"thesis", r"dissertation"],
            "Coursework & Term Papers": [r"coursework", r"term paper", r"assignment", r"essay"],
            "Certificates & Diplomas": [r"certificate", r"diploma", r"certification", r"degree"],
            "Tests & Quizzes": [r"test", r"quiz", r"exam", r"midterm", r"final exam"],
            "Answer Keys & Solutions": [r"answer key", r"solution", r"solutions manual"],
            "Presentations": [r"presentation", r"slides", r"powerpoint", r"keynote"],
            "Formal Documents & Correspondence": [r"letter", r"memo", r"memorandum", r"contract", r"agreement", r"official document"],
            "Books & Textbooks": [r"book", r"textbook", r"manual", r"e-book"],
            "Learning Materials & Study Guides": [r"study guide", r"notes", r"handout", r"worksheet", r"learning material"],
            "Reports": [r"report", r"summary", r"analysis", r"findings"]
        }

    def categorize_text(self, text: str, categories: list[str]) -> str | None:
        """
        Categorizes the given text into one of the provided categories using mock logic.

        Args:
            text: The text content to categorize.
            categories: A list of category names to choose from.

        Returns:
            The name of the matched category, or None if no category matches or text is empty.
        """
        if not text or not text.strip():
            return None

        lower_text = text.lower()

        for category_name in categories:
            if category_name in self._category_keywords:
                keywords = self._category_keywords[category_name]
                for keyword_pattern in keywords:
                    if re.search(keyword_pattern, lower_text):
                        return category_name
        
        return None

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    categorizer = LLMCategorizer()
    
    sample_texts = [
        ("This is my master's thesis on AI.", "Theses & Dissertations"),
        ("Please find attached the certificate of completion.", "Certificates & Diplomas"),
        ("Here are the slides for my presentation.", "Presentations"),
        ("Weekly project report.", "Reports"),
        ("Solutions for chapter 5 exercises.", "Answer Keys & Solutions"),
        ("A short quiz about historical dates.", "Tests & Quizzes"),
        ("Term paper on climate change.", "Coursework & Term Papers"),
        ("Textbook for Introduction to Physics.", "Books & Textbooks"),
        ("My study guide for the upcoming exam.", "Learning Materials & Study Guides"),
        ("An official letter from the university.", "Formal Documents & Correspondence"),
        ("This document is completely unrelated.", None),
        ("", None)
    ]

    print("Running mock categorization tests:")
    for i, (text_to_test, expected_category) in enumerate(sample_texts):
        predicted_category = categorizer.categorize_text(text_to_test, PREDEFINED_CATEGORIES)
        print(f"Test {i+1}:")
        print(f"  Text: \"{text_to_test[:50]}...\"")
        print(f"  Expected: {expected_category}")
        print(f"  Predicted: {predicted_category}")
        assert predicted_category == expected_category, f"Mismatch for text: {text_to_test}"
        print(f"  Result: {'PASS' if predicted_category == expected_category else 'FAIL'}")
        print("-" * 20)
    
    print("\nTesting with a category not in PREDEFINED_CATEGORIES (should not match based on internal keywords):")
    custom_categories = ["Custom Category A", "Theses & Dissertations"]
    text_custom = "This is a thesis."
    predicted_custom = categorizer.categorize_text(text_custom, custom_categories)
    print(f"  Text: \"{text_custom}\"")
    print(f"  Categories: {custom_categories}")
    print(f"  Expected (based on internal keywords): Theses & Dissertations")
    print(f"  Predicted: {predicted_custom}")
    assert predicted_custom == "Theses & Dissertations"
    print(f"  Result: {'PASS' if predicted_custom == 'Theses & Dissertations' else 'FAIL'}")
    print("-" * 20)

    print("\nTesting with a category that has keywords but is not in the input list:")
    text_only_internal = "This is a thesis."
    predicted_only_internal = categorizer.categorize_text(text_only_internal, ["Random Category"])
    print(f"  Text: \"{text_only_internal}\"")
    print(f"  Categories: {['Random Category']}")
    print(f"  Expected: None (because 'Theses & Dissertations' is not in the provided list)")
    print(f"  Predicted: {predicted_only_internal}")
    assert predicted_only_internal is None
    print(f"  Result: {'PASS' if predicted_only_internal is None else 'FAIL'}")
    print("-" * 20)

    print("All mock tests passed (if no assertion errors).")
