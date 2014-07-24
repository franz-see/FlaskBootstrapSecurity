app.controller('TodoCtrl', ['$scope', '$modal', '$filter', 'todoService', function($scope, $modal, $filter, Todo) {
    $scope.DATE_FORMAT = app.DATE_FORMAT;

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
                     { field: 'date', displayName: 'Date', width: '20%', cellFilter: "date:'" + $scope.DATE_FORMAT + "'", cellClass : 'rightAlign' }
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

    $scope.openSaveModal = function (selectedTodo) {
        $modal.open({
            templateUrl: 'todoAddModal.html',
            controller: function ($scope, $modalInstance, todos, selectedTodo, DATE_FORMAT) {
                $scope.DATE_FORMAT = DATE_FORMAT;
                $scope.todo = selectedTodo ? new Todo(selectedTodo) : new Todo({'date':new Date()});

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
                            var index = todos.indexOf(selectedTodo);
                            if (~index) {
                                todos[index].id = resp.id;
                                todos[index].item = resp.item;
                                todos[index].date = resp.date;
                            } else {
                                todos.unshift(resp);
                            }
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
                },
                selectedTodo: function() {
                    return selectedTodo;
                },
                DATE_FORMAT : function() {
                    return $scope.DATE_FORMAT;
                }
            }
        });
    };

    $scope.openDeleteConfirmationModal = function () {
        $modal.open({
            templateUrl: 'todoDeleteConfirmation.html',
            controller: function ($scope, $modalInstance, todos, hasSelectedTodo, selectedTodo) {
                $scope.selectedTodo = selectedTodo;
                console.log("hasSelectedTodo: " + hasSelectedTodo);
                console.log("selectedTodo: " + JSON.stringify($scope.selectedTodo));

                $scope.ok = function () {
                    if (!hasSelectedTodo) {
                        return;
                    }
                    Todo.delete({'id':$scope.selectedTodo.id}, function(resp) {
                        var index = todos.indexOf(selectedTodo);
                        if (~index) {
                            todos.splice(index, 1);
                        }
                        $modalInstance.close();
                    });
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
            },
            size: 'sm',
            resolve: {
                todos: function () {
                    return $scope.todos;
                },
                hasSelectedTodo : function() {
                    return $scope.selectedTodos.length;
                },
                selectedTodo: $scope.getSelectedTodo
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

