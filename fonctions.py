import streamlit as st
from st_keyup import st_keyup
import data as d
from PIL import Image
from PIL import ImageDraw
from urllib.request import urlopen


def convert_to_readable(name):
    words = []
    current_word = name[0]
    for char in name[1:]:
        if char.isupper() or char.isdigit():
            words.append(current_word)
            current_word = char
        else:
            current_word += char
    words.append(current_word)
    
    readable_name = ' '.join(word.capitalize() for word in words)
    readable_name = readable_name.replace("Percentage", "%")
    if readable_name == 'Accurate Final Third Passes':
        readable_name = 'Accurate Final\nThird Passes'
    if readable_name == 'Accurate Long Balls %':
        readable_name = 'Accurate Long\nBalls %'
    
    return readable_name 

def example():
    st.write("## Notice how the output doesn't update until you hit enter")
    out = st.text_input("Normal text input")
    st.write(out)
    st.write("## Notice how the output updates with every key you press")
    out2 = st_keyup("Keyup input")
    st.write(out2)
    
def convert_market_value(value):
    # Ensure value is treated as string
    if isinstance(value, float):
        return value
    if value == '-' or value == '':
        return None
    value = value.replace('€', '')
    if 'k' in value:
        return float(value.replace('k', '')) * 1e3
    if 'm' in value:
        return float(value.replace('m', '')) * 1e6
    return float(value)


position_mapping=d.position_mapping
def get_position_group(position):
    for group, positions in position_mapping.items():
        if position in positions:
            return group
    return None

def filter_positions(user_choices):
    
    selected_positions = []
    for choice in user_choices:
        selected_positions.extend(position_mapping.get(choice, []))
    
    return selected_positions

def get_color_category(value, df, stat, reverse_stats):
    q1, q2, q3 = df[stat].quantile([0.25, 0.5, 0.75])
    
    reverse = stat in reverse_stats
    
    if not reverse:
        if value < q1:
            return '#fe003e'  # Bottom 25%
        elif value < q2:
            return '#ffa500'  # 25-50%
        elif value < q3:
            return '#ffef01'  # 50-75%
        else:
            return '#00ff1d'  # Top 25%
    else:
        if value > q3:
            return '#fe003e'  # Top 25%
        elif value > q2:
            return '#ffa500'  # 50-75%
        elif value > q1:
            return '#ffef01'  # 25-50%
        else:
            return '#00ff1d'  # Bottom 25%
        
def get_image_output(URL):
    img = Image.open(urlopen(URL))
    # Create a mask
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    # Apply the mask to the image
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0), mask)
    return output