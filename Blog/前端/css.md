## `position: relative;` 和 `position: absolute;`

`position: relative;` 和 `position: absolute;` 是 CSS 中用于定位元素的两种不同方式，它们有以下主要区别：

1. 定位参考点：
   - `position: relative;`：元素相对于自身在正常文档流中的位置进行定位。换句话说，它是相对于元素自身的原始位置进行定位。
   - `position: absolute;`：元素相对于最近的具有定位（非 `static`）属性的父元素进行定位。如果没有具有定位属性的父元素，那么元素将相对于视口进行定位。
2. 文档流影响：
   - `position: relative;`：元素仍然保持在正常文档流中，不会对其他元素的布局产生影响。其他元素在页面上仍然占据着它们原始的位置。
   - `position: absolute;`：元素脱离了正常文档流，不再占据原始位置，可能会对其他元素的布局产生影响，使它们填补被移除元素的空间。
3. 偏移属性：
   - `position: relative;`：通过使用 `top`、`right`、`bottom` 和 `left` 属性来进行相对定位。这些属性控制元素相对于原始位置的偏移量。
   - `position: absolute;`：同样可以使用 `top`、`right`、`bottom` 和 `left` 属性来进行定位，但它们是相对于定位父元素的边界进行定位的。
4. 嵌套关系：
   - `position: relative;`：定位相对于自身，因此可以嵌套使用多个相对定位的元素，每个元素都相对于其包含的相对定位元素进行定位。
   - `position: absolute;`：通常在嵌套的情况下，相对于最近的具有定位属性的父元素进行定位。如果所有父元素都没有定位属性，则相对于视口定位。

总之，`position: relative;` 用于相对定位元素，保留元素在文档流中的位置，而 `position: absolute;` 用于绝对定位元素，根据最近的具有定位属性的父元素来定位，同时脱离文档流。选择哪种定位方式取决于您的设计需求和元素的关系。



## `position: absolute;`是以谁为定位位置



`position: absolute;` 是相对于最近的具有定位（非 `static`）属性的父元素来进行定位的。

如果您的元素具有 `position: absolute;`，但没有明确指定 `top`、`right`、`bottom` 或 `left` 属性，它将以最近的具有定位属性的父元素的左上角为参考点。

如果没有任何具有定位属性的父元素，那么这个元素将以浏览器窗口（视口）的左上角为参考点。

以下是一个示例，以说明元素的定位是相对于最近的具有定位属性的父元素：

```
htmlCopy code<div style="position: relative;">
  <div style="position: absolute; top: 20px; left: 20px;">相对于这个父元素定位</div>
</div>
```

在这个示例中，内部的 `<div>` 元素使用 `position: absolute;` 进行定位，它的定位参考点是包含它的具有 `position: relative;` 的父元素的左上角。

请注意，如果没有明确的定位父元素，元素将以视口为参考点。因此，确保理解元素的定位上下文，以便您可以正确地定位元素。