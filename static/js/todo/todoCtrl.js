app.controller('TodoCtrl', ['$scope', '$modal', 'todoService', function($scope, $modal, Todo) {
    $scope.todos = [];
    $scope.totalServerItems = 0;

    $scope.format = app.dateFormat;

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
                     { field: 'date', displayName: 'Date', width: '20%', cellFilter: "date:'" + app.dateFormat + "'", cellClass : 'rightAlign' }
        ]
    };

    $scope.getPagedDataAsync = function () {
        setTimeout(function () {
            var queryParams = {
                's' : $scope.pagingOptions.pageSize,
                'p' : $scope.pagingOptions.currentPage
            };
            Todo.query(queryParams, function(value) {
                $scope.todos = value['results'];
                $scope.totalServerItems = value['total_size'];
                if (!$scope.$$phase) {
                    $scope.$apply();
                }
            });
        }, 100);
    };

    $scope.getPagedDataAsync();

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        if (newVal !== oldVal && newVal.currentPage !== oldVal.currentPage) {
          $scope.getPagedDataAsync();
        }
    }, true);
    $scope.$watch('filterOptions', function (newVal, oldVal) {
        if (newVal !== oldVal) {
          $scope.getPagedDataAsync();
        }
    }, true);

    $scope.openModal = function () {
        $modal.open({
            templateUrl: 'todoAddCtrl.html',
            controller: function ($scope, $modalInstance, todos) {
                $scope.todo = new Todo({'date':new Date()});

                $scope.dateOptions = {
                    formatYear: 'yy',
                    startingDay: 1
                };

                $scope.openDatePicker = function ($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = true;
                };

                $scope.ok = function () {
                    $scope.todo.$save()
                        .then(function(resp) {
                            todos.unshift(resp);
                        });
                    $modalInstance.close();
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
            },
            size: 'sm',
            resolve: {
                todos: function () {
                    return $scope.todos;
                }
            }
        });
    };

}]);

