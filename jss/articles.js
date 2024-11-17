document.addEventListener('DOMContentLoaded', () => {
    // Path to the JSON file
    const jsonFilePath = 'assets/articles.json';
    const articlesList = document.getElementById('articles-list');

    // Fetch JSON data
    fetch(jsonFilePath)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load JSON: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Populate the list with data
        data.forEach(article => {
          const li = document.createElement('li');
          li.innerHTML = `
            <p><a href="${article.link}" target="_blank">${article.title} </a> (${article.year}).
            <b>${article.authors}</b>.</p>
            <p>${article.abstract}</p>
          `;
          articlesList.appendChild(li);
        });
        if (window.MathJax) {
          MathJax.typeset();
        }
      })
      .catch(error => {
        console.error('Error loading JSON:', error);
        articlesList.innerHTML = '<li>Error loading articles.</li>';
      });
  });
