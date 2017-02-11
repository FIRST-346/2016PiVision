'use strict';

/**
 * @ngdoc directive
 * @name grapherApp.directive:LineChart
 * @description
 * # LineChart
 */
angular.module('grapherApp')
  .directive('LineChart', function () {
    return {
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the LineChart directive');
      }
    };
  });
