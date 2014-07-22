var app =  angular.module('todo',['ngResource', 'ngGrid']);

app.factory('todoService', ['$resource', function ($resource) {
    return $resource('/api/todo/:id', {}, {
      query: { method: 'GET' } 
    });
}]);

app.controller('TodoCtrl', ['$scope', 'todoService', function($scope, todoService) {
    $scope.todos = [];
    $scope.totalServerItems = 0;

    $scope.filterOptions = {
        filterText: "",
        useExternalFilter: true
    };
    $scope.pagingOptions = {
        pageSizes: [5, 10, 20],
        pageSize: 5,
        currentPage: 1
    };  
    $scope.gridOptions = { 
        data: 'todos',
        enablePaging: true,
        showFooter: true,
        totalServerItems:'totalServerItems',
        pagingOptions: $scope.pagingOptions,
        filterOptions: $scope.filterOptions,
        columnDefs: [{ field: 'item', displayName: 'Item', width: '80%' },
                     { field: 'date', displayName: 'Date', width: '20%', cellFilter: "date:'MMMM d, yyyy'", cellClass : 'rightAlign' }
        ]
    }

    $scope.getPagedDataAsync = function (pageSize, page) {
        setTimeout(function () {
            var queryParams = {
                's' : $scope.pagingOptions.pageSize,
                'p' : $scope.pagingOptions.currentPage
            };
            todoService.query(queryParams, function(value) {
                $scope.todos = value['results'];
                $scope.totalServerItems = value['total_size'];
                if (!$scope.$$phase) {
                    $scope.$apply();
                }
            });
        }, 100);
    };
    
    $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    
    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        if (newVal !== oldVal && newVal.currentPage !== oldVal.currentPage) {
          $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        }
    }, true);
    $scope.$watch('filterOptions', function (newVal, oldVal) {
        if (newVal !== oldVal) {
          $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        }
    }, true);
    
}]);

