import re



# CONVERSATION A IMPORTER ICI !!!!!!!!!!!!
custom_conversations = [
    {"author": "Teacher", "content": "What is the square root of 16?"},
    {"author": "Teacher", "content": "What is the capital of France?"},
    {"author": "Teacher", "content": "What is the largest mammal on Earth?"},
]

# Convert the list of conversations into a JavaScript object string
conversations_js = (
    "{\n" +
    ",\n".join(
        f"conversation{i+1}: [\n    {{ author: \"{conv['author']}\", content: \"{conv['content']}\" }}\n]"
        for i, conv in enumerate(custom_conversations)
    ) +
    "\n}"
)

# Read the content of the JS file
with open("java.js", "r") as js_file:
    js_content = js_file.read()

# Replace the conversations object in the JS content with the custom one
js_content = re.sub(
    r"const conversations = \{[\s\S]*?\};",
    f"const conversations = {conversations_js};",
    js_content,
)

# Write the modified content back to the JS file
with open("java.js", "w") as js_file:
    js_file.write(js_content)
