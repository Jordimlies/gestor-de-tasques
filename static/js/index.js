document.addEventListener('DOMContentLoaded', function () {
    var altaPrioritat = document.getElementById('alta-prioritat');
    var baixaPrioritat = document.getElementById('baixa-prioritat');

    new Sortable(altaPrioritat, {
        animation: 150,
        onEnd: function (evt) {
            updateTaskOrder('alta');
        }
    });

    new Sortable(baixaPrioritat, {
        animation: 150,
        onEnd: function (evt) {
            updateTaskOrder('baixa');
        }
    });

    function updateTaskOrder(prioritat) {
        var tasks = document.querySelectorAll('.tasques-prioritat.' + prioritat + ' .tasca');
        var order = [];
        tasks.forEach(function (task, index) {
            order.push({
                id: task.getAttribute('data-id'),
                new_order: index + 1
            });
        });

        fetch('/update_task_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prioritat: prioritat,
                order: order
            })
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Order updated successfully');
                  location.reload();
              } else {
                  console.error('Failed to update order');
              }
          });
    }
});