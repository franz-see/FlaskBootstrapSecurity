var app =  angular.module('todo',['ngResource', 'ngGrid']);

app.factory('todoService', ['$resource', function ($resource) {
    return $resource('/api/todo/:id', {}, {
      query: { method: 'GET', isArray:true }
    });
}]);

app.controller('TodoCtrl', ['$scope', 'todoService', function($scope, todoService) {
    $scope.todos = [];
    $scope.gridOptions = { 
        data: 'todos',
        columnDefs: [{ field: 'item', displayName: 'Item', width: '80%' },
                     { field: 'date', displayName: 'Date', width: '20%', cellFilter: "date:'MMMM d, yyyy'", cellClass : 'rightAlign' }
        ]
    }
    $scope.todos = todoService.query();
}]);
