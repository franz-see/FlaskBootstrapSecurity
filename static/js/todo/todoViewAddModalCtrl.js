app.controller('TodoModalCtrl', ['$scope', '$modal', 'todoService', function ($scope, $modal, Todo) {
    $scope.format = app.dateFormat;
    $scope.openModal = function (size) {

        var modalInstance = $modal.open({
            templateUrl: 'todoAddCtrl.html',
            controller: function ($scope, $modalInstance) {
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
                    $scope.todo.$save();
                    $modalInstance.close();
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
            },
            size: size,
            resolve: {
            }
        });

        modalInstance.result.then(function (selectedItem) {
        }, function () {
        });
    };
}]);
