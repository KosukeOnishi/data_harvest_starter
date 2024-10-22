# Data Harvest Starter

This project provides sample code to help you implement completions using the OpenAI or Perplexity. It serves as a template that can be easily adapted for tasks such as data collection, analysis, or other AI-driven operations. Whether you are gathering information from different sources or automating requests to AI services, this project offers a structured starting point.

Feel free to fork and customize it to suit your specific needs.

## Use Cases

The project allows you to use either OpenAI or PerplexityAI depending on the task. PerplexityAI is preferred for gathering online data, while OpenAI is ideal for tasks that require structured outputs in JSON format, image processing, or more advanced operations. Below are some concrete and attractive examples of how you can leverage both services for data collection:

- **Extracting and Structuring Data from Photos**
  You can use OpenAI's image processing capabilities to automatically extract text from a list of photos and structure the data into a CSV format. For example, if you have a collection of restaurant menu photos, OpenAI's API can analyze the images, identify the menu items and their prices, and then format this information into structured data for further use.

- **Automated Survey Data Processing**
  Automatically collect survey responses with PerplexityAI and use OpenAI to process the data, transforming unstructured responses into JSON format or generating summaries and key

## Requirements

To run this project, the following libraries are required:

- `openai`
- `python-dotenv`
- `requests`

You can install these with the following command:

```bash
pip install -r requirements.txt
```

## Environment Variables

Before running the project, create a `.env` file and set the following environment variables:

```
OPENAI_API_KEY=your_OpenAI_API_key
PPLX_API_KEY=your_PPLX_API_key
```

## Usage

### Starter Script

Running `starter.py` will retrieve responses based on prompts using the OpenAI API.

```bash
python starter.py
```

### Image Processing

Running `openai_image.py` will encode a specified image and send it to the OpenAI API to get a response.

```bash
python templates/openai_image.py
```

### Concurrent Requests

Running `concurrent_request.py` will send requests simultaneously to multiple cities.

```bash
python templates/concurrent_request.py
```

## Notes

- Be aware of the limitations on API usage and monitor the frequency of requests.
- The `.gitignore` file includes the environment variable file and data folders.

## License

This project is licensed under the MIT License.