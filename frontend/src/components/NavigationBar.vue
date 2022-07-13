<template>
  <div>
    <h1>hallo</h1>
    <vue-navigation-bar :options="navbarOptions" />


  </div>
</template>


<script>
    export default {
        data() {
            return{
                navbarOptions: {
                    elementId: "main-navbar",
                    isUsingVueRouter: true,
                    mobileBreakpoint: 992,
                    brandImagePath: "./",
                    brandImageAltText: "brand-image",
                    collapseButtonOpenColor: "#661c23",
                    collapseButtonCloseColor: "#661c23",
                    showBrandImageInMobilePopup: true,
                    ariaLabelMainNav: "Main Navigation",
                    tooltipAnimationType: "shift-away",
                    tooltipPlacement: "bottom",
                }
            }
        }
    }

</script>