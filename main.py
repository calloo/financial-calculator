import webview
from webview import Window

from core.calculator import Calculator


def main(win: Window):
    win.evaluate_js(
        """
        (async() => {
            const ctx = document.getElementById('myChart').getContext('2d');
            const investment_timespan = document.querySelector('#investment_timespan');
            const investment_timespan_text = document.querySelector('#investment_timespan_text');
            const future_balance = document.querySelector('#future_balance');
            const depositSelector = document.querySelector('#initial_deposit');
            const estimatedReturnSelector = document.querySelector('#estimated_return');
            const contributionSelector = document.querySelector('#contribution_amount');
            const spriteSelector = document.querySelector('#sprite');

            const updateChart = async () => {
                const {labels, principal_dataset, earnings_dataset} = await pywebview.api.calculate_future_values();

                chart.data.labels = labels;
                chart.data.datasets[0].data = principal_dataset.data;
                chart.data.datasets[1].data = earnings_dataset.data;
                chart.update();
                const balance = await pywebview.api.get_amount('future_balance');
                future_balance.innerHTML = '$' + balance.toFixed(2);
                const goal = await pywebview.api.get_amount('goal');
                
                if (balance >= goal) {
                    const sprite = await pywebview.api.get_sprite();
                    if (sprite) {
                        spriteSelector.src = sprite;
                    }
                } else {
                    spriteSelector.src = '';
                }
            }

            const changeHandler = async (dom, action = 'set') => {
                const name = dom.getAttribute('id');
                const min = parseFloat(dom.getAttribute('min'));
                const max = parseFloat(dom.getAttribute('max'));
                const oldValue = dom.dataset.value || dom.defaultValue || 0;
                let newValue = parseFloat(dom.value.replace(/\$/, ''));
                const step = ['investment_timespan'].includes(name) ? newValue: parseFloat(dom.getAttribute('step')) || 1;

                if (isNaN(parseFloat(newValue))) {
                    newValue = oldValue;
                } else {
                    newValue = await pywebview.api.change_amount(name, step, action);
                    newValue = newValue < min ? min : newValue > max ? max : newValue;
                }

                dom.dataset.value = newValue;
                dom.value = (dom.dataset.prepend || '') + newValue + (dom.dataset.append || '');
                await updateChart();
            };

            investment_timespan.value = await pywebview.api.get_amount('investment_timespan');
            investment_timespan_text.innerHTML = investment_timespan.value + ' years';
            depositSelector.dataset.value = await pywebview.api.get_amount('initial_deposit');
            depositSelector.value = '$' + depositSelector.dataset.value;
            contributionSelector.dataset.value = await pywebview.api.get_amount('contribution_amount');
            contributionSelector.value = '$' + contributionSelector.dataset.value;
            estimatedReturnSelector.dataset.value = await pywebview.api.get_amount('estimated_return');
            estimatedReturnSelector.value = estimatedReturnSelector.dataset.value + '%';
            
            depositSelector.addEventListener('change', function(){ changeHandler(this) });
            estimatedReturnSelector.addEventListener('change', function(){ changeHandler(this) });
            contributionSelector.addEventListener('change', function(){ changeHandler(this) });
            investment_timespan.addEventListener('change', async function () {
                changeHandler(this);
                investment_timespan_text.innerHTML = this.value + ' years';
                await updateChart();
            });
            investment_timespan.addEventListener('input', function () {
                investment_timespan_text.innerHTML = this.value + ' years';
            });
            
            const contribution_period = await pywebview.api.get_amount('contribution_period');
            const compound_period = await pywebview.api.get_amount('compound_period');
            
            Array.from(document.querySelectorAll('[name="contribution_period"], [name="compound_period"]'))
            .forEach(radio => {
            if (radio.name.includes('contribution') && parseInt(radio.value) === contribution_period) {
                radio.checked = true;
            } else if (radio.name.includes('compound') && parseInt(radio.value) === compound_period) {
                radio.checked = true;
            }
            radio.addEventListener('change', async function() {
                if (this.checked) {
                    await pywebview.api.change_amount(this.getAttribute('name'), parseInt(this.value), 'set');
                }
                await updateChart();
            });
            });

            Array.from(document.querySelectorAll('[data-counter]'))
            .forEach(
                button => button.addEventListener('click', function () {
                    var field = document.querySelector('[name="' + this.dataset.field + '"]'),
                        action = this.dataset.counter;

                    if (field) {
                        changeHandler(field, action);
                    }
                })
            );

            const {label, ...data} = await pywebview.api.calculate_future_values();
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {label, datasets: Object.values(data)},
                options: {
                    legend: {
                        display: false
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function (tooltipItem, data) {
                                console.log(data.datasets[tooltipItem.datasetIndex]);
                                return data.datasets[tooltipItem.datasetIndex].label + ': $' + tooltipItem.yLabel;
                            }
                        }
                    },
                    responsive: true,
                    scales: {
                        xAxes: [{
                            stacked: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Year'
                            }
                        }],
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                callback: function (value) {
                                    return '$' + value;
                                }
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Balance'
                            }
                        }]
                    }
                }
            });
        })();
        """
    )
    pass


if __name__ == '__main__':
    window = webview.create_window('Financial Calculator', 'web/index.html', js_api=Calculator())
    webview.start(main, window, gui='cef', debug=True)
