document.addEventListener('DOMContentLoaded', () => {
    const jsonFilePath = 'assets/articles.json';
    const sections = {
        "last_month": document.getElementById('articles-list-last-month'),
        "last_year": document.getElementById('articles-list-last-year'),
        "last_5_years": document.getElementById('articles-list-last-5-years'),
        "all_time": document.getElementById('articles-list-all-time'),
    };

    fetch(jsonFilePath)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to load JSON: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        Object.keys(sections).forEach(range => {
          const articlesList = sections[range];
          data[range].forEach(article => {
            const li = document.createElement('li');
            li.innerHTML = `
              <p><a href="${article.link}" target="_blank">${article.title} </a> (${article.year}).
              <b>${article.authors}</b>.</p>
              <p>${article.abstract}</p>
            `;
            articlesList.appendChild(li);
          });
        });
        if (window.MathJax) {
          MathJax.typeset();
        }
      })
      .catch(error => {
        console.error('Error loading JSON:', error);
        Object.values(sections).forEach(articlesList => {
          articlesList.innerHTML = '<li>Error loading articles.</li>';
        });
      });
  });
