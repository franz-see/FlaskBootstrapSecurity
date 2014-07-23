app.controller('TodoModalCtrl', ['$scope', '$modal', function ($scope, $modal) {
    $scope.openModal = function (size) {

        var modalInstance = $modal.open({
            templateUrl: 'todoAddCtrl.html',
            controller: function ($scope, $modalInstance) {
                $scope.ok = function () {
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
