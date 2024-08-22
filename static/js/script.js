document.querySelectorAll('.favorite-btn').forEach(button => {
    button.addEventListener('click', () => {
        const playerId = button.getAttribute('data-id');
        fetch('/toggle_favorite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `player_id=${playerId}`
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'added') {
                  button.textContent = '-';
                  button.closest('tr').classList.add('favorite-highlight');
              } else if (data.status === 'removed') {
                  button.textContent = '⭐';
                  button.closest('tr').classList.remove('favorite-highlight');
              }
          });
    });
});
