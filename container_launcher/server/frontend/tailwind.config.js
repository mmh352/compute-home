module.exports = {
    content: [
        './src/**/*.svelte',
    ],
    theme: {
        fontFamily: {
            sans: 'Arial,Helvetica,sans-serif',
        },
        extend: {
            colors: {
                blue: {
                    100: '#9fbbdc',
                    200: '#7aa2cf',
                    300: '#5689c1',
                    400: '#326fb4',
                    DEFAULT: '#0e56a7',
                    600: '#0d4d96',
                    700: '#0b4586',
                    800: '#0a3c75',
                    900: '#083464',
                },
                pink: {
                    100: '#f3a1cd',
                    200: '#ef7eba',
                    300: '#eb5ba7',
                    400: '#e63794',
                    DEFAULT: '#e21481',
                    600: '#cb1274',
                    700: '#b51067',
                    800: '#9e0e5a',
                    900: '#880c4d',
                },
                turquoise: {
                    100: '#9bcdd4',
                    200: '#76bac4',
                    300: '#51a8b3',
                    400: '#2b95a3',
                    DEFAULT: '#068293',
                    600: '#057584',
                    700: '#056876',
                    800: '#045b67',
                    900: '#044e58',
                },
                orange: {
                    100: '#edb5a2',
                    200: '#e7997f',
                    300: '#e07e5c',
                    400: '#da6239',
                    DEFAULT: '#d34616',
                    600: '#be3f14',
                    700: '#a93812',
                    800: '#94310f',
                    900: '#7f2a0d',
                },
                'light-gray': {
                    DEFAULT: '#e9eaea',
                },
                gray: {
                    100: '#dcddde',
                    200: '#cfd0d1',
                    300: '#c1c3c5',
                    400: '#b4b6b8',
                    DEFAULT: '#a7a9ac',
                    600: '#96989b',
                    700: '#86878a',
                    800: '#757678',
                    900: '#646567',
                },
                black: {
                    100: '#999999',
                    200: '#737373',
                    300: '#4d4d4d',
                    400: '#262626',
                    DEFAULT: '#000000',
                },
                white: {
                    DEFAULT: '#ffffff',
                    600: '#f6f8fa',
                },
                red: {
                    100: '#fdf0f2',
                    400: '#e42448',
                    DEFAULT: '#cd2041',
                },
                green: {
                    DEFAULT: '#008a00',
                    600: '#008500',
                },
                cream: {
                    400: '#f8f6ed',
                    DEFAULT: '#ece7ce',
                }
            },
        },
    },
    plugins: [],
}
