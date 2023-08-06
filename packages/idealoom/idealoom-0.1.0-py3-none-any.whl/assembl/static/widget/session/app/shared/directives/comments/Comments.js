SessionApp.directive('comments', [
    '$http',
    '$rootScope',
    'UtilsService',
    'WidgetService',
    'UserService',

    function($http, $rootScope, UtilsService, WidgetService, UserService) {

      return {
        restrict:'E',
        scope: {
          idea:'=idea',
          widget:'=widget',
          reply:'=reply'
        },
        templateUrl: 'app/shared/directives/comments/comments.html',
        link: function($scope, element, attrs) {

          $scope.formData = {};
          $scope.comments = [];

          // when the session end up, switch to read only mode
          if ($scope.widget.settings.endDate) {
            $scope.readOnly = new Date().getTime() > new Date($scope.widget.settings.endDate).getTime();
          }

          $scope.$watch('idea.proposed_in_post.selected', function(checked) {
            if (checked) {
              $scope.checked = true;
            } else {
              $scope.checked = false;
            }

            angular.forEach($scope.comments, function(com) {
              com.selected = $scope.checked;
            });
          });

          $scope.$watch('message', function(value) {

            switch (value){
              case 'commentSubIdea:success':
                $scope.getCommentsFromSubIdea();
                $scope.message = null; // reset message value, in order to hear another change if the user posts another message
                break;
              case 'commentSubIdea:error':
                $scope.message = null; // reset message value, in order to hear another change if the user posts another message
                break;
            }
          }, true);

          $scope.getUserForComment = function() {

            var config = $scope.$parent.$state.params.config;

            var id = decodeURIComponent(config).split('/')[1],
                widget = WidgetService.get({id: id}).$promise;

            widget.then(function(w) {

              $scope.discussion = w.discussion;

              var discussion_id = w.discussion.split('/')[1];

              return UserService.get({id: discussion_id}).$promise;

            }).then(function(user) {
              user.avatar_url_base = user.avatar_url_base + 30;
              $scope.currentUser = user;
            });
          }

          $scope.findUntranslated = function(langstring) {
            for (var i in langstring.entries) {
                var entry = langstring.entries[i];
                if (entry["@language"].indexOf("-x-mtfrom-") < 0) {
                    return entry.value;
                }
            }
          };

          /**
           * get all comments from a sub idea
           */
          $scope.getCommentsFromSubIdea = function() {

            var rootUrl = $scope.idea.widget_add_post_endpoint,
                comments = [];

            $http.get(rootUrl).then(function(response) {
              angular.forEach(response.data, function(com) {
                var user_id = com.idCreator.split('/')[1];

                com.date = UtilsService.getNiceDateTime(com.date);
                com.avatar = '/user/id/' + user_id + '/avatar/30';
                console.log("checking loadComments");
                // See comment in RateController to understand rootScope use.
                if ($rootScope.selectedComments === undefined) {
                  com.showSelected = false;
                } else {
                  com.showSelected = true;
                  com.selected = $rootScope.selectedComments.indexOf(com['@id']) >= 0;
                }

                comments.push(com);
              })

              return comments;

            }).then(function(commments) {

              angular.forEach(commments, function(c) {

                var urlRoot = UtilsService.getURL(c.idCreator);

                $http.get(urlRoot).then(function(response) {

                  c.username = response.data.name;
                });

              });

              $scope.comments = commments;
            });
          }

          /**
           * Comment an idea from creativity session
           */
          $scope.commentSubIdea = function() {

            var rootUrl = $scope.idea.widget_add_post_endpoint,
                user_id = $scope.widget.user['@id'];

            var data = {
              "@type": 'WidgetPost',
              "subject": '',
              "body": {
                "@type": "LangString", "entries": [{
                    "@type": "LangStringEntry", "value": $scope.formData.comment,
                    "@language": "und"}]},
              "idCreator": user_id
            }

            if (data.body && data.idCreator && rootUrl) {

              $http({
                method:'POST',
                url: rootUrl,
                data: JSON.stringify(data),
                headers: {'Content-Type': 'application/json'}
              }).success(function() {

                $scope.message = "commentSubIdea:success";
                $scope.formData.comment = null;
                $scope.displayBox = false;

              }).error(function() {

                $scope.message = "commentSubIdea:success";
              });

            }
          }

          $scope.expand = function(e) {

            var elm = angular.element(e.currentTarget);

            elm.css('overflow', 'hidden');
            elm.css('height', 0);
            elm.css('height', elm[0].scrollHeight + 'px');
          }

          /**
           * init method
           * */
          $scope.getCommentsFromSubIdea();

          $scope.getUserForComment();

        }
      }
    }]);
