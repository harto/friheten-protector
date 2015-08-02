(defun raspberry-push-command ()
  (expand-file-name "dev/raspberry-push" (ftf-project-directory)))

(defun raspberry-push ()
  (start-process "raspberry-push" nil (raspberry-push-command)))

(add-hook 'after-save-hook #'raspberry-push)
