'use strict';

/**
 * @ngdoc overview
 * @name grapherApp
 * @description
 * # grapherApp
 *
 * Main module of the application.
 */
angular
  .module('grapherApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
	.when('/graph', {
		templateUrl: 'views/graph.html',
		controller: 'GraphCtrl',
		controllerAs: 'Graph'
	})
      .otherwise({
        redirectTo: '/'
      });
  });
