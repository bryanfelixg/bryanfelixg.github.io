document.addEventListener('DOMContentLoaded', function () {
    const postContent = document.getElementById('post-content');
    const headings = postContent.querySelectorAll('h1, h2, h3, h4, h5, h6');
    const sidebar = document.querySelector('.sidebar ul'); // Select the existing sidebar UL
  
    headings.forEach(heading => {
      const link = document.createElement('a');
      link.href = "#" + heading.id;
      link.textContent = heading.textContent;
  
      const listItem = document.createElement('li');
      listItem.appendChild(link);
      sidebar.appendChild(listItem);
    });
  });
  