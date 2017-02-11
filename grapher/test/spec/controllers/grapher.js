'use strict';

describe('Controller: GrapherCtrl', function () {

  // load the controller's module
  beforeEach(module('grapherApp'));

  var GrapherCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    GrapherCtrl = $controller('GrapherCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(GrapherCtrl.awesomeThings.length).toBe(3);
  });
});
