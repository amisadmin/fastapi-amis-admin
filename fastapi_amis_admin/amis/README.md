## Amis introduction

[amis](https://github.com/baidu/amis) is a low-code front-end framework developed by the `Baidu` team, which uses `JSON`
Configuring to generate pages can reduce the workload of page development and greatly improve efficiency. `python amis`
Based on `baidu amis`, the `amis` data structure is converted to the corresponding python data model through [pydantic](https://pydantic-docs.helpmanual.io), and some common methods are added.

## Amis Highlights

- **No need to know front-end**: Inside Baidu, most of the amis users have never written front-end pages before, nor `JavaScript`, but they can make professional and complex back-end interfaces, which is the same as all other front-ends.
  UI library can't do it;
- **Not affected by front-end technology updates**: The oldest amis page in Baidu was created more than 6 years ago and is still in use, while the `Angular/Vue/React` of that year
  Versions are now obsolete, and the popular `Gulp` was also used by `Webpack`
  Instead, if these pages do not use amis, the maintenance cost will now be high;
- **Enjoy the continuous upgrade of amis**: amis has been improving the interactive experience of details, such as the freezing of the first row of the table, the lack of lag under the big data of the drop-down box, etc. The previous JSON configuration does not need to be modified at all;
- You can **completely** use the [visual page editor](https://aisuda.github.io/amis-editor-demo/) to make pages: general front-end visual editors can only be used for static prototypes, while
  friends
  The page made by the visual editor can be launched directly.
- **Provide a complete interface solution**: Other UI frameworks must use JavaScript to assemble business logic, while amis only needs JSON
  Configuration can complete complete function development, including functions such as data acquisition, form submission and verification, and the resulting page can be launched directly without secondary development;
- **A large number of built-in components (120+), one-stop solution**: Most of other UI frameworks only have the most common components. If you encounter some less commonly used components, you have to find a third party yourself, and these third parties Components are often inconsistent in presentation and interaction, and the integration effect is not good.
  friends
  There are a large number of built-in components, including business components such as rich text editor, code editor, diff, conditional combination, real-time log, etc. Most of the middle and background page development only needs to understand amis;
- **Support extension**: In addition to low-code mode, you can also extend components through [custom components](https://baidu.gitee.io/amis/zh-CN/docs/extend/internal), in fact
  amis can be used as normal UI
  Libraries are used to achieve a mixed mode of 90% low code and 10% code development, which improves efficiency without losing flexibility;
- **Container supports infinite nesting**: various layout and presentation needs can be met through nesting;
- **Experiencing a long-term practical test**: amis is widely used within Baidu, **created 50,000 pages in more than 6 years**, from content review to machine management, from data analysis to model training, amis
  Satisfies a variety of page needs, the most complex page has more than 10,000 lines of JSON
  configuration.

## Install

```bash
pip install amis 
```

## Simple example

**main.py**:

```python
from amis.components import Page

page = Page(title='title', body='Hello World!')
# output as json
print(page.amis_json())
# output as dict
print(page.amis_dict())
# output page html
print(page.amis_html())
```

## Development documentation

Reference: [Amis official documentation](https://baidu.gitee.io/amis/zh-CN/docs/index)

## Dependent projects

- [pydantic](https://pydantic-docs.helpmanual.io/)

- [amis](https://baidu.gitee.io/amis)

## agreement

The project follows the Apache2.0 license agreement.


