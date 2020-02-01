$(function() {
    $.each(data, (i, data) => {
        let [question, answer_options, counts] = data;

        $('#results').append(document.querySelector('template').content.cloneNode(true));
        $('canvas').last().attr('id', 'question' + i);
        $('h5').last().html(question);
        let ctx = document.getElementById('question' + i).getContext('2d');

        let myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: answer_options,
                datasets: [{
                    label: '# of Votes',
                    data: counts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            precision: 0,
                            callback: function (value) {
                                return value.toLocaleString('de-DE', {style:'percent'});
                            }
                        }
                    }]
                },
                responsive: false
            }
        });

    });

});