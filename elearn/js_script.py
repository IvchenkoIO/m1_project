import os
import re

from easylearn import settings


def make_conv(question_list):
    custom_conversations = []
    for item in question_list:
        print(item.title)
        custom_conversations.append({"author": "Teacher", "content": item.question})
# CONVERSATION A IMPORTER ICI !!!!!!!!!!!!
    # Convert the list of conversations into a JavaScript object string
    conversations_js = (
        "{\n" +
        ",\n".join(
            f"conversation{i+1}: [\n    {{ role: \"{conv['author']}\", content: \"{conv['content']}\" }}\n]"
            for i, conv in enumerate(custom_conversations)
        ) +
        "\n}"
    )

    # Read the content of the JS file
    java_path=os.path.join(settings.BASE_DIR, 'elearn/static/js/java.js')
    with open(java_path, "r") as js_file:
        js_content = js_file.read()

    # Replace the conversations object in the JS content with the custom one
    js_content = re.sub(
        r"const conversations = \{[\s\S]*?\};",
        f"const conversations = {conversations_js};",
        js_content,
    )

    # Write the modified content back to the JS file
    with open(java_path, "w") as js_file:
        js_file.write(js_content)
