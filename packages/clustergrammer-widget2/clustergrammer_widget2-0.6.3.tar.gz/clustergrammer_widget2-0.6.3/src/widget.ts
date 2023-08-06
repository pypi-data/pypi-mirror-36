// Copyright (c) Nicolas Fernandez.
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  EXTENSION_SPEC_VERSION
} from './version';

import cgm_fun from 'clustergrammer-gl';

import * as d3 from 'd3';

console.log('version 0.6.3')
// console.log(cgm_fun);
// console.log(d3)

export
class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      value : 'default-string',
      network: ''
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static model_name = 'ExampleModel';
  static model_module = 'clustergrammer_widget2';
  static model_module_version = EXTENSION_SPEC_VERSION;
  static view_name = 'ExampleView';  // Set to null if no view
  static view_module = 'clustergrammer_widget2';   // Set to null if no view
  static view_module_version = EXTENSION_SPEC_VERSION;
}


function make_viz(args){
  var inst_container = document.getElementById(args.container_name)
  console.log('inst_container_2', inst_container)
  args.container = inst_container;
  var cgm = cgm_fun(args)
  console.log('making clustergram in make_viz');
  console.log(cgm);
}

console.log(make_viz)


export
class ExampleView extends DOMWidgetView {
  render() {

    this.value_changed();
    // this.model.on('change:value', this.value_changed, this);

    console.log('\n**********************************************');
    console.log('rendering!!');
    console.log('**********************************************');

    var inst_network_string = this.model.get('network');

    var inst_network = JSON.parse(inst_network_string);

    console.log(inst_network)

    var container_name = this.cid;

    // the cid appears to be the container id, which gives a unique view number
    console.log('container_name', container_name)

    // widget-subarea appears to be limited to a width of ~960px in nbviewer
    var inst_container = d3.select(this.el)
        .append('div')
        .classed('clustergrammer_glidget', true)
        .attr('id', container_name)
        .style('width', '900px')
        .style('height', '1035px')
        .style('border', '2px solid #eee');

    var container_id = '#'+container_name;

    console.log(container_name, inst_container, container_id);

    var heatmap_width = 900;

    // define arguments object
    var args = {
        'container_name': container_name,
        'network': inst_network,
        'viz_width' : heatmap_width,
        'viz_height': heatmap_width
    };

    console.log(args);

    setTimeout(make_viz, 10, args);

  }

  value_changed() {
    console.log('CHANGING')
  }
}
