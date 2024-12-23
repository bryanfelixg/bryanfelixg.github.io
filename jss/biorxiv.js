document.addEventListener('DOMContentLoaded', () => {
  const jsonFilePath = 'assets/biorxiv.json';
  const articlesList = document.getElementById('articles-biorxiv');

  fetch(jsonFilePath)
      .then(response => {
          if (!response.ok) {
              throw new Error(`Failed to load JSON: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          // Ensure `data` is an array and iterate over it
          data.forEach(article => {
              const li = document.createElement('li');
              li.innerHTML = `
                  <p><a href="${article.pdf_link}" target="_blank">${article.title} </a> (${article.posted}).
                  <b>${article.authors}</b>.</p>
                  <p>${article.abstract}</p>
              `;
              articlesList.appendChild(li);
          });

          // Re-render MathJax content if needed
          if (window.MathJax) {
              MathJax.typeset();
          }
      })
      .catch(error => {
          console.error('Error loading JSON:', error);
          articlesList.innerHTML = '<li>Error loading articles.</li>';
      });
});
