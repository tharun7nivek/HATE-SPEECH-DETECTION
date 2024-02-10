const form = document.getElementById('news-form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const input = document.getElementById('news-text').value;

  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `text=${encodeURIComponent(input)}`,
    });

    if (response.ok) {
      const predictionIndex = (await response.json()).prediction;
      const resultDiv = document.getElementById('prediction-result');
      if (predictionIndex === 0) {
        resultDiv.innerText = 'The text contains Hate Speech';
      } else if (predictionIndex === 1) {
        resultDiv.innerText = 'The text is Offensive Language';
      } else if (predictionIndex === 2) {
        resultDiv.innerText = 'The text is Normal';
      }
    } else {
      console.error('Request failed:', response.status);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
});
