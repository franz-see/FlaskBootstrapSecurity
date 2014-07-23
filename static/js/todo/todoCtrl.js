app.controller('TodoCtrl', ['$scope', '$modal', 'todoService', function($scope, $modal, Todo) {
    $scope.DATE_FORMAT = app.dateFormat;

    $scope.todos = [];
    $scope.totalServerItems = 0;
    $scope.selectedTodos = [];

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
        multiSelect: false,
        selectedItems: $scope.selectedTodos,
        enablePaging: true,
        showFooter: true,
        totalServerItems:'totalServerItems',
        pagingOptions: $scope.pagingOptions,
        filterOptions: $scope.filterOptions,
        columnDefs: [{ field: 'item', displayName: 'Item', width: '80%' },
                     { field: 'date', displayName: 'Date', width: '20%', cellFilter: "date:'" + app.dateFormat + "'", cellClass : 'rightAlign' }
        ]
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        if (newVal !== oldVal && newVal.currentPage !== oldVal.currentPage) {
          _getPagedDataAsync();
        }
    }, true);
    $scope.$watch('filterOptions', function (newVal, oldVal) {
        if (newVal !== oldVal) {
          _getPagedDataAsync();
        }
    }, true);

    $scope.openAddModal = function () {
        $modal.open({
            templateUrl: 'todoAddModal.html',
            controller: function ($scope, $modalInstance, todos) {
                $scope.todo = new Todo({'date':new Date()});

                $scope.isOpen = true;

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

    $scope.openDeleteConfirmationModal = function () {
        $modal.open({
            templateUrl: 'todoDeleteConfirmation.html',
            controller: function ($scope, $modalInstance, hasSelectedTodo, selectedTodo) {
                $scope.selectedTodo = selectedTodo;
                console.log("hasSelectedTodo: " + hasSelectedTodo);
                console.log("selectedTodo: " + JSON.stringify($scope.selectedTodo));

                $scope.ok = function () {
                    if (!hasSelectedTodo) {
                        return;
                    }
                    Todo.delete({'id':$scope.selectedTodo.id}, function(resp) {
                        _getPagedDataAsync();
                        $modalInstance.close();
                    });
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
            },
            size: 'sm',
            resolve: {
                selectedTodo: $scope.getSelectedTodo,
                hasSelectedTodo : function() {
                    return $scope.selectedTodos.length;
                }
            }
        });
    };

    $scope.getSelectedTodo = function() {
        return $scope.selectedTodos.length ? $scope.selectedTodos[0] : {};
    };

    var _getPagedDataAsync = function () {
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

    _getPagedDataAsync();

}]);

