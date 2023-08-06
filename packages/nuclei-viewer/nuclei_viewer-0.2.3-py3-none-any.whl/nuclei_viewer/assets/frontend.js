
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    )
}

String.prototype.trunc = String.prototype.trunc ||
      function(n){
          return (this.length > n) ? this.substr(0, n-1) + '...' : this;
      };

function bindEvents() {
    const id = 'graph'
    const gd = document.getElementById(id);
    const btn_add = document.getElementById('add');
    const color = {'centroid': 'OrangeRed', 'ctc': 'Crimson', 'nuclei': 'LightSkyBlue', '+': 'Orange'}

    // workaround: https://github.com/plotly/plotly.js/issues/2504 
    gd.on('plotly_click', (eventData) => {
        // toggle selection
        var g = eventData.points[0].data.legendgroup
        if (g == 'centroid')
            return
        var l = eventData.points[0].curveNumber;
        var c = eventData.points[0].data.line.color;
        g = (g == 'ctc') ? 'nuclei' : 'ctc';
        var update = {'line': {color: color[g]}, 'legendgroup': g};
        Plotly.restyle(id, update, [l]);
    });

    gd.on('plotly_selected', (eventData) => {
        var x = eventData.lassoPoints.x.map(i => ~~i);
        var y = eventData.lassoPoints.y.map(j => ~~j);
        var m = uuidv4();
        x.push(x[0]);
        y.push(y[0]);
        Plotly.addTraces(id, {
            showlegend: false,
            legendgroup: 'new',
            name: m.trunc(10),
            mode: 'lines',
            line: {'color': color['+']},
            x: x,
            y: y,
            customdata: [m],
            fill: 'toself',
            opacity: 0.3
        });
        Plotly.relayout(id, { dragmode: 'pan' });
    });

    btn_add.onclick = () => {
        Plotly.relayout(id, { dragmode: 'lasso' });
    };
};

setTimeout(bindEvents, 2000);
