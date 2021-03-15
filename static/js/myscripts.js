function graphs(y) {

  am4core.ready(function() {

    am4core.useTheme(am4themes_animated);
    var chart = am4core.create(`chart_${y}`, am4charts.XYChart)

    var xAxis = chart.xAxes.push(new am4charts.CategoryAxis())
    xAxis.dataFields.category = 'category'
    xAxis.renderer.cellStartLocation = 0.1
    xAxis.renderer.cellEndLocation = 0.9
    xAxis.renderer.grid.template.location = 0;
    xAxis.renderer.inside = true;
    xAxis.renderer.labels.template.valign = "top";
    xAxis.renderer.labels.template.fontSize = 12;

    var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
    yAxis.min = 0;
    yAxis.max = 6000;
    yAxis.renderer.labels.template.fontSize = 10;


    function createSeries(value, name) {
      var series = chart.series.push(new am4charts.ColumnSeries())
      series.dataFields.valueY = value
      series.dataFields.categoryX = 'category'
      series.fill = am4core.color("#573c73");
      series.stroke = am4core.color("#573c73");
      series.name = name

      series.columns.template.tooltipText = "{name}: [bold]{valueY}[/]";
      series.columns.template.width = am4core.percent(90);
      series.columns.template.column.cornerRadiusTopLeft = 3;
      series.columns.template.column.cornerRadiusTopRight = 3;
      series.columns.template.column.fillOpacity = 0.9;

      var bullet = series.bullets.push(new am4charts.LabelBullet);
      bullet.label.text = "{name}";
      bullet.label.fontSize = 8;
      /*bullet.label.rotation = 90;*/
      bullet.label.truncate = false;
      bullet.label.hideOversized = false;
      bullet.locationY = 1;
      bullet.dy = 10;
      chart.paddingBottom = 30;
      chart.maskBullets = false;
      return series;
    }

    /*chart.dataSource.url = "{% url 'stops:trying' %}";*/
    chart.dataSource.url = `../stops/templates/stops/${y}.json`;

    createSeries('1', 'U#1');
    createSeries('2', 'U#2');
    createSeries('3', 'U#3');
    createSeries('4', 'U#4');

  }); // end am4core.ready()
}
graphs(2019)
graphs(2018)
graphs(2020)
graphs(2021)
