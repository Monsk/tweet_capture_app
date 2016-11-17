
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { FilterChart as Component} from 'pyxley';
    var filter_style = "'btn-group'";
var dynamic = true;
var charts = [{"type": "MetricsGraphics", "options": {"url": "/mgchart/", "chart_id": "mychart", "params": {"y_accessor": "y", "x_accessor": "x", "target": "#mychart", "title": "Line Chart", "buffer": 8, "small_width_threshold": 160, "top": 40, "bottom": 30, "height": 200, "transition_on_update": "true", "right": 40, "left": 40, "animate_on_load": "true", "small_height_threshold": 120, "init_params": {"Data": "Steps"}, "width": 450, "description": "Line Chart"}}}];
var filters = [{"type": "SelectButton", "options": {"default": "Steps", "items": ["Calories Burned", "Steps", "Distance", "Floors", "Minutes Sedentary", "Minutes Lightly Active", "Minutes Fairly Active", "Minutes Very Active", "Activity Calories"], "alias": "Data", "label": "Data"}}];
    ReactDOM.render(
        <Component
        filter_style = { filter_style }
dynamic = { dynamic }
charts = { charts }
filters = { filters } />,
        document.getElementById("component_id")
    );
    