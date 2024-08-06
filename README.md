# PDF Query Assistant
Welcome to PDF Query Assistant, a handy tool that empowers users to ask questions about PDF documents and receive accurate answers. This README.md file provides an overview of the project, its features, and instructions for usage.

## Features
Upload PDF: Users can easily upload their PDF files through the user-friendly interface.

Ask Questions: Once the PDF is uploaded, users can ask questions related to the content of the document.

Intelligent Query Assistant: The system uses advanced natural language processing to understand and analyze the questions, providing relevant and precise answers.

User-Friendly Interface: The interface is designed for simplicity, ensuring a seamless and intuitive experience for users.

## Tech Stack: 
Python

Streamlit

Langchain

Pinecone

Firebase

HTML

CSS

## API used:
OpenAI 

Pinecone

## Getting Started

1. Clone the project repository:
     https://github.com/TirthrajDharane1703/pdf_query_assistant-main.git
2. Create python environment
3. Install  dependencies using the provided requirements.txt file:
     pip install -r requirements.txt
4. Obtain OpenAI API key and add in .env file
5. Create Index in Pinecone with deimnsions 1536
6. Add Pinecone API key, enviorment key and index name in main.py file
7. Create project in Firebase and add the Database url and .json file path in main.py file
8. Run the application in you environment using:
       streamlit run main.py

## Contributing
We welcome contributions from the community! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Special thanks to the contributors and the open-source community for their valuable input and support.

Happy querying! 🚀
