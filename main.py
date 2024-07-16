import streamlit as st
from openai import OpenAI

def generate_story(prompt):
  story_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[
          {"role": 'system', "content": "You are a creative story writer and everyone in the world is looking forward to your new story"},
          {"role": 'user', "content": f'{prompt}'},
      ],
      max_tokens=100,
      temperature=0.8
  )
  return story_response.choices[0].message.content

def create_design_prompt(story_response):
  design_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[
          {
              "role": 'system',
              "content": """Based on the story given, you will design a detailed image prompt for the cover image of this story.
              The image prompt should include the theme of the story with relevant color, suitable for adults. The output should be within 100 characters"""
          },
          {
              "role": 'user',
              "content": story_response
          }
      ],
      max_tokens=100,
      temperature=0.8
  )
  design_prompt = design_response.choices[0].message.content
  return design_prompt

def generate_cover_image(design_prompt):
  cover_response =  client.images.generate(
      model='dall-e-2',
      prompt=f"{design_prompt}",
      size='256x256',
      quality='standard',
      n=1
  )
  image_url = cover_response.data[0].url
  return image_url

api_key = st.secrets['OpenAI_Key']
client = OpenAI(api_key=api_key)


with st.form("Why this section cant be empty"):
  st.markdown("<h1 style='text-align: center; color: Pink;'>Welcome to the Story Generator</h1>", unsafe_allow_html=True)
  st.write("")
  prompt = st.text_input(label = "Please enter some keywords to generate a story")
  st.write("")
  submitted = st.form_submit_button("Submit")
  if submitted:
    story = generate_story(prompt)
    st.write(story)
    design_prompt = create_design_prompt(story)
  
    st.write("**Here is your refined story version:**")
    st.write(design_prompt)

    st.write("**Here is your refined cover image:**")
    image_url = generate_cover_image(design_prompt)
    st.image(image_url)

