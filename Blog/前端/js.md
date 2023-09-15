## 监听事件

1. **DOMContentLoaded**：用于监听文档的 DOMContentLoaded 事件，表示在 HTML 文档完全加载和解析后触发的事件。除了DOMContentLoaded事件，还有许多其他事件可以监听
2. **click**：用于监听元素的点击事件，当用户点击元素时触发。
3. **keydown**：监听键盘按键按下事件，通常用于捕捉用户按下某个键盘键的动作。
4. **keyup**：监听键盘按键释放事件，通常用于捕捉用户释放某个键盘键的动作。
5. **mouseenter** 和 **mouseleave**：用于监听鼠标进入和离开元素的事件。
6. **submit**：监听表单提交事件，当用户提交表单时触发。
7. **input**：监听输入框内容改变事件，当输入框的值发生改变时触发。
8. **resize**：监听窗口大小改变事件，当浏览器窗口大小改变时触发。
9. **scroll**：监听滚动事件，当页面滚动时触发。
10. **load**：监听页面加载完成事件，当页面及其所有资源加载完成后触发。
11. **focus** 和 **blur**：用于监听元素获得焦点和失去焦点的事件。
12. **mousedown** 和 **mouseup**：分别用于监听鼠标按下和释放事件。
13. **mousemove**：监听鼠标移动事件，通常用于实现鼠标悬停效果或拖拽操作。
14. **contextmenu**：监听右键点击事件，当用户右键点击元素时触发。
15. **dblclick**：监听双击事件，当用户双击元素时触发。
16. **keydown** 和 **keyup**：用于监听键盘按键按下和释放事件，可捕获特定键盘键的动作。
17. **touchstart**、**touchmove** 和 **touchend**：用于监听触摸设备上的触摸事件。
18. **dragstart**、**dragenter**、**dragover**、**dragleave** 和 **drop**：用于实现拖拽和拖放操作的事件。
19. **focusin** 和 **focusout**：分别用于监听元素获得和失去焦点的事件，与 **focus** 和 **blur** 不同，这两个事件可以冒泡。
20. **input** 和 **change**：用于监听表单元素的值改变事件，通常用于实时反馈用户输入。
21. **animationstart**、**animationiteration** 和 **animationend**：用于监听 CSS 动画的开始、迭代和结束事件。
22. **transitionend**：用于监听 CSS 过渡效果结束事件。
23. **online** 和 **offline**：用于监听网络连接状态的事件。
24. **beforeunload**：用于监听页面即将关闭的事件，通常用于提示用户保存未保存的数据。
25. **visibilitychange**：用于监听页面可见性状态的改变，当用户切换标签页或最小化浏览器时触发。
26. **hashchange**：用于监听 URL 的哈希部分改变事件。



```javascript
const accountInput = document.getElementById('account');

accountInput.addEventListener('input', restrictInput1);

function restrictInput1(event) {
    const input = event.target;
    const inputValue = input.value;

    // 使用正则表达式检查输入是否包含非字母和非数字字符
    if (/[^a-zA-Z0-9]/.test(inputValue)) {
        // 如果包含非法字符，将输入值重置为空
        input.value = '';
        Qmsg.warning('仅限输入数字和字母', {
            autoClose:true,
            timeout:5000
        });
    }
}
```

在这个代码中，`event` 参数是一个事件对象，它是由浏览器传递给事件处理函数的。事件对象包含了与事件相关的信息，允许你访问事件的各种属性和方法。

事件对象的属性和方法可以根据不同的事件类型而变化，但通常它会包含以下常见的属性和方法：

1. `event.target`: 获取触发事件的DOM元素，也就是事件的目标元素。
2. `event.type`: 获取事件的类型，例如 "click"、"input" 等。
3. `event.preventDefault()`: 阻止事件的默认行为，比如阻止一个链接的跳转或表单的提交。
4. `event.stopPropagation()`: 阻止事件冒泡，即阻止事件从目标元素向上传播到父级元素。
5. `event.keyCode` 或 `event.key`: 用于键盘事件，获取按下的键的键码或键名。
6. `event.clientX` 和 `event.clientY`: 用于鼠标事件，获取鼠标指针相对于视口（viewport）的坐标。
7. `event.pageX` 和 `event.pageY`: 用于鼠标事件，获取鼠标指针相对于文档页面的坐标。

在你的代码中，`event` 参数是事件处理函数 `restrictInput1` 的参数，它用于监听 `input` 事件。当用户在输入框中输入内容时，`event` 对象将包含与输入事件相关的信息，例如输入框的值和事件类型，以便你可以根据需要执行相应的操作。

在这个特定的代码中，它使用了 `event.target` 来获取触发事件的输入框元素，然后通过 `input.value` 获取输入框的值，以检查输入是否包含非字母和非数字字符，如果包含则重置输入值为空，并显示一个警告消息。

## `querySelector()`

`querySelector` 是 JavaScript 中的一个方法，用于通过 CSS 选择器来选择文档中的元素。它允许你以简洁的方式选择一个或多个满足条件的元素。

以下是 `querySelector` 和 `querySelectorAll` 的用法：

1. **querySelector(selector)**：选择第一个匹配 `selector` 的元素。

   ```
   const element = document.querySelector(".my-class"); // 选择第一个具有 "my-class" 类的元素
   ```

2. **querySelectorAll(selector)**：选择所有匹配 `selector` 的元素，并返回一个 NodeList（类似数组的对象）。

   ```
   const elements = document.querySelectorAll("p"); // 选择所有 <p> 元素
   ```

CSS 选择器是一种用于选择 HTML 元素的语法。例如，`.my-class` 选择所有具有 `my-class` 类的元素，`#my-id` 选择具有 `my-id` id 的元素，`p` 选择所有 `<p>` 元素等等。

使用这些方法，你可以在 JavaScript 中方便地选择和操作 HTML 元素。