'use strict';

/**
 * @ngdoc function
 * @name grapherApp.controller:GrapherCtrl
 * @description
 * # GrapherCtrl
 * Controller of the grapherApp
 */
angular.module('grapherApp')
  .controller('GraphCtrl', function () {
    var vm = this;
	vm.data = [{time:0,values:{value1:1,value2:2}},{time:1,values:{value1:2,value2:-1}}];
  });
