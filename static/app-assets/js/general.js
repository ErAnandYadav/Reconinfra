"use strict";
var KTSignupGeneral = (function () {
  var e,
    t,
    a,
    r,
    s = function () {
      return 100 === r.getScore();
    };
  return {
    init: function () {
      (e = document.querySelector("#kt_sign_up_form")),
        (t = document.querySelector("#kt_sign_up_submit")),
        (r = KTPasswordMeter.getInstance(
          e.querySelector('[data-kt-password-meter="true"]')
        )),
        (a = FormValidation.formValidation(e, {
          fields: {
            "first_name": {
              validators: { notEmpty: { message: "First Name is required" } },
            },
            "last_name": {
              validators: { notEmpty: { message: "Last Name is required" } },
            },
            "phone_number": {
              validators: { notEmpty: { message: "Phone Number is required" } },
            },
            email: {
              validators: {
                regexp: {
                  regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                  message: "The value is not a valid email address",
                },
                notEmpty: { message: "Email address is required" },
              },
            },
            password: {
              validators: {
                notEmpty: { message: "The password is required" },
                callback: {
                  message: "Please enter valid password",
                  callback: function (e) {
                    if (e.value.length > 0) return s();
                  },
                },
              },
            },
            "confirm-password": {
              validators: {
                notEmpty: { message: "The password confirmation is required" },
                identical: {
                  compare: function () {
                    return e.querySelector('[name="password"]').value;
                  },
                  message: "The password and its confirm are not the same",
                },
              },
            },
            toc: {
              validators: {
                notEmpty: {
                  message: "You must accept the terms and conditions",
                },
              },
            },
          },
          plugins: {
            trigger: new FormValidation.plugins.Trigger({
              event: { password: !1 },
            }),
            bootstrap: new FormValidation.plugins.Bootstrap5({
              rowSelector: ".fv-row",
              eleInvalidClass: "",
              eleValidClass: "",
            }),
          },
        })),
        t.addEventListener("click", function (s) {
          s.preventDefault(),
            a.revalidateField("password"),
            a.validate().then(function (a) {
              "Valid" == a
                ? (t.setAttribute("data-kt-indicator", "on"),
                  (t.disabled = !0),
                  setTimeout(function () {
                    t.removeAttribute("data-kt-indicator"),
                      (t.disabled = !1);
                      
                  }, 1500))
                : Swal.fire({
                    
                  });
            });
        }),
        e
          .querySelector('input[name="password"]')
          .addEventListener("input", function () {
            this.value.length > 0 &&
              a.updateFieldStatus("password", "NotValidated");
          });
    },
  };
})();
KTUtil.onDOMContentLoaded(function () {
  KTSignupGeneral.init();
});
