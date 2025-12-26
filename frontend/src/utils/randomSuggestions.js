/**
 * 随机生成记忆建议数据
 */

// 预设的标题模板
const titleTemplates = [
  '今天学到的知识',
  '重要的工作笔记',
  '生活中的感悟',
  '技术问题解决方案',
  '读书笔记',
  '会议记录',
  '灵感想法',
  '待办事项',
  '学习心得',
  '项目总结',
  '日常记录',
  '思考片段',
  '经验总结',
  '问题反思',
  '计划安排'
]

// 预设的内容模板
const contentTemplates = [
  '今天在工作中遇到了一个有趣的问题，通过查阅资料和思考，最终找到了解决方案。这个过程让我学到了很多。',
  '阅读了一篇关于技术架构的文章，其中提到的设计模式很值得深入学习。需要找时间实践一下。',
  '和同事讨论了一个项目的优化方案，大家的想法都很有价值。记录下来以便后续参考。',
  '今天完成了一个重要的功能开发，虽然过程中遇到了一些困难，但最终都解决了。',
  '学习了一个新的编程技巧，可以大大提高开发效率。需要在实际项目中应用。',
  '参加了一个技术分享会，讲者分享的经验很有启发性。值得深入思考和学习。',
  '今天处理了一个紧急bug，虽然花费了不少时间，但学到了很多调试技巧。',
  '阅读了一本好书，其中某些观点让我对工作有了新的认识。',
  '完成了一个小项目的重构，代码质量得到了明显提升。',
  '今天和团队成员进行了深入的讨论，大家对项目的方向有了更清晰的认识。',
  '学习了一个新的工具，可以简化日常的开发工作流程。',
  '今天解决了一个困扰很久的问题，感觉很有成就感。',
  '记录一下今天的工作进展，明天需要继续完成剩余的任务。',
  '思考了一个新的产品功能，需要进一步验证可行性。',
  '总结一下本周的工作，下周需要重点关注几个关键问题。'
]

// 预设的标签库
const tagOptions = [
  '工作', '学习', '技术', '生活', '重要', '待办', '想法', '笔记',
  '问题', '解决方案', '经验', '总结', '计划', '阅读', '会议', '项目'
]

/**
 * 随机选择一个数组元素
 */
function randomChoice(array) {
  return array[Math.floor(Math.random() * array.length)]
}

/**
 * 随机选择多个不重复的元素
 */
function randomChoices(array, count) {
  const shuffled = [...array].sort(() => 0.5 - Math.random())
  return shuffled.slice(0, Math.min(count, array.length))
}

/**
 * 生成一条随机记忆建议
 */
export function generateRandomSuggestion() {
  const title = randomChoice(titleTemplates)
  const content = randomChoice(contentTemplates)
  const tagCount = Math.floor(Math.random() * 3) + 1 // 1-3个标签
  const tags = randomChoices(tagOptions, tagCount)

  return {
    title,
    content,
    tags
  }
}

/**
 * 生成多条随机记忆建议
 * @param {number} count 生成数量，默认3条
 */
export function generateRandomSuggestions(count = 3) {
  const suggestions = []
  for (let i = 0; i < count; i++) {
    suggestions.push(generateRandomSuggestion())
  }
  return suggestions
}

