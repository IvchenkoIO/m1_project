from bs4 import BeautifulSoup

with open("index1.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

# Find the 'ul' element with the id 'my-list'
my_list = soup.find("ul", id="conversations")

new_values = ["Question1", "Question2", "Question3", "Question4","question5"]

for item in my_list.find_all("li"):
    item.extract()

# Add exactly 5 'li' elements with data-conversation-id attributes
for index in range(len(new_values)):
    new_item = soup.new_tag("li")
    new_item.string = f"Item {index + 1}"
    new_item['data-conversation-id'] = f'conversation{index + 1}'
    my_list.append(new_item)


for index, item in enumerate(my_list.find_all("li")):
    item.string = new_values[index]
    item['data-conversation-id'] = f'conversation{index + 1}'

# Write the modified HTML to a new file
with open("output.html", "w", encoding="utf-8") as file:
    file.write(str(soup))
