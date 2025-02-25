<template>
  <div class="body-container ft13">
    <div class="focus-gpt-demo-container">
      <!-- 第一步： 您还没有选择需要提问的数据表 -->
      <template v-if="currentStep === 1">
        <div class="select-table-container flex-column-container">
          <h1 class="text-center">请您先选择需要提问的数据表</h1>
          <div class="select-table-content flex-content">
            <template v-if="getTableStatus">
              <p class="text-center">获取数据表中....</p>
            </template>
            <template v-else-if="getTableErrorMsg">
              <p class="text-center error-msg" v-text="getTableErrorMsg"></p>
            </template>
            <template v-else-if="!selectTableList || !selectTableList.length">
              <p class="text-center error-msg">当前环境没有可用的数据表</p>
            </template>
            <template v-else-if="selectTableList && selectTableList.length">
              <div class="flex-column-container">
                <div class="flex-row-container">
                  <div class="flex-content" v-text="selectTableErrorMsg"></div> 
                  <button class="primary-button go-to-chat-button"
                          v-bind:class="{'disabled': selectTableStatus}"
                          v-on:click="submitGoChat()" >进入聊天 >> </button>
                </div>
                <div class="select-table-list-container flex-row-container flex-content mt10">
                  <template v-for="(table , $index) in selectTableList">
                    <div class="select-table-item text-clip"
                        v-bind:key="'table-name-' + table.tblName + '-' + $index"
                        v-bind:title="table.tblName"
                        v-bind:class="{current: currentTable && currentTable.tblName === table.tblName}"
                        v-on:click="currentTable = table ; selectTableErrorMsg = '';"
                        v-text="table.tblName"></div>
                  </template>
                  <div class="select-table-item text-clip null-item"></div>
                  <div class="select-table-item text-clip null-item"></div>
                  <div class="select-table-item text-clip null-item"></div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </template>
      <!-- 第二步： 选择表后聊天 -->
      <template v-else-if="currentStep > 1">
        <div class="chat-message-container flex-column-container">
          <h1 class="text-center">您可以开始问数啦</h1>
          <div class="chat-message-list flex-content">
            <template v-for="(chat , $index) in currentChatList">
              <div class="chat-message-item" v-bind:key="'chat-' + chat.chatId + '-' + $index"
                   v-bind:class="[ chat.from ]">
                <div class=" flex-row-container">
                  <template v-if="chat.from === 'user'">
                    <div class="chat-user-avatar icon-user-avatar"></div>
                  </template>
                  <template v-else>
                    <div class="chat-user-avatar icon-gpt-avatar"></div>                  
                  </template>
                  <div class="chat-message-content flex-content ml10">
                    <div class="text-break ft-bold ft14" v-text="chat.content"></div>
                  </div>
                </div>
                <template v-if="chat.type === 'tableInfo'">
                    <div class="mb15 mt10 ml50">
                      <div class="ft14 mb10" style="word-break: break-all;">
                          <!--<span class="focus-icon ft16 icon-chart-table"></span>-->
                          <span class="focus-icon-text">{{currentTable.tblName }} 中包含以下字段  ：</span>
                      </div>

                      <div class="mb5" 
                           v-for="(column , $index) in currentTable.columns"
                           v-bind:key="'column-item-' + column.colDisplayName + '-' + $index">
                            {{ $index + 1 }}. {{ column.colDisplayName }}
                            <template v-if="column.dataType === 'timestamp'">
                                <span class="color-main-blue ml5">[日期]</span>
                            </template>
                            <template v-else-if="column.dataType === 'string'">
                                <span class="color-main-blue ml5">[字符串]</span>
                            </template>
                            <template v-else>
                                <span class="color-main-green ml5">[数字]</span>
                            </template>
                        </div>
                    </div>

                </template>

                <template v-if="chat.type === 'answer'">
                  <div class="mb15 mt10 ml50">
                    <div class="text-break ft-bold ft14 mb10" v-text="chat.question"></div>
                    <div class="gpt-chat-answer-container mt10">
                      <DfChartContainer :ref="'myDfChartContainer-' + chat.answerId"
                                       class="gpt-answer-content"></DfChartContainer>
                    </div>
                  </div>
                </template>
                
              </div>
            </template>

          </div>
          <div class="chart-input-container mt10">
            <div class="search-chart-input-container flex-row-container" @keyup.stop.prevent="">
              <!-- 输入框 没有开启小慧时，用户边输入边分词 -->
              <textarea class="flex-content input-dom ml10"
                            v-model="currentQuestion"
                            v-on:keypress.enter.stop.prevent="sendQuestionToGpt"
                            placeholder="请输入您的问题"></textarea>
              <button type="button"
                      class="primary-button mr10"
                      v-bind:class="{'disabled' : sendQuestionStatus }"
                      v-on:click="sendQuestionToGpt()">发送</button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
/**
 * 这是一个本地构建FocusGPT的demo, 主要有三部
 * 1. 让用户选择表（暂时只支持单表）
 * 2. 使用选择的表初始化聊天，得到chatId
 * 3. 在chatId的基础下提问，如果可以画图则画图 ； 否则就显示回复文字 ；
 * */
import 'datafocus-chart/dist/datafocus.chart.css' ;
import {DfChartContainer} from 'datafocus-chart/dist/datafocus.chart.js' ;

export default {
  name: 'App',
  components: {
    DfChartContainer
  } ,
  data(){
    return {
      currentStep: 1 ,         // 当前步骤

      getTableStatus: false ,
      getTableErrorMsg: '' ,
      selectTableList: null ,   // 可以选择的表

      selectTableStatus: false ,
      selectTableErrorMsg: '' ,
      currentTable: null ,      // 选择提问的表
      currentChatId: '' ,       // 当前的chatId
      currentChatList: [] ,     // 聊天记录

      currentQuestion: '' ,
      sendQuestionStatus: false ,
    }
  } ,
  mounted: function(){
      // 1. 初始化页面时，获取可以选择的表，让用户选择提问的数据表
      const theVue = this ;
      theVue.getTableList();
  } ,
  methods: {
    // 1. 获取可以选择的表,使用API接口 POST /listTables?name=过滤表名
    getTableList: function(callback){
      // 获取可以选择的表
      const theVue = this ;
      theVue.getTableStatus = true ;
      theVue.axios({
        url: '/listTables' ,
        method: 'post' ,
        params: { name: ''} ,
        data: { datasource: null }
      }).then(function(response){
        if(response.status === 200){
          const result = response.data ;
          if(result && result.success){
            theVue.selectTableList = result.data ;
            typeof callback === 'function' && callback();
          }else{
            console.error('接口报错');
            theVue.getTableErrorMsg = '接口报错' ;
          }
        }else{
          console.error('接口无法访问');
          theVue.getTableErrorMsg = '接口无法访问' ;
        }
      }).catch(function(error){
        console.log(error) ;
        theVue.getTableErrorMsg = '接口无法访问' ;
      }).finally(function(){        
        theVue.getTableStatus = false ;
      }) ;
    } ,

    // 2. 选择表后去聊天
    submitGoChat: function(){
      const theVue = this ;
      if(!theVue.currentTable) { theVue.selectTableErrorMsg = '请您先选择提问的数据表' ; return false ; }
      theVue.selectTableStatus = true ;
      theVue.selectTableErrorMsg = '' ;
      theVue.axios({
        url: '/init' ,
        method: 'post' ,
        data: { name: theVue.currentTable.tblName , language: 'chinese' , datasource: null}
      }).then(function(response){
        if(response.status === 200){
          const result = response.data ;
          if(result && result.success){
              theVue.currentStep = 2 ;
              theVue.currentChatList = [{
                from: 'system' ,
                content: '您好，我是FocusGPT，您刚选择了数据表 { ' + theVue.currentTable.tblName +' } , 我可以回答您关于它的问题 。' ,
                type: 'tableInfo' 
              }] ;
              theVue.currentChatId = result.data ;
          }else{
            theVue.selectTableErrorMsg = '接口报错' ;
          }
        }else{
          theVue.selectTableErrorMsg = '接口无法访问' ;
        }
      }).catch(function(error){
        console.info(error);
        theVue.selectTableErrorMsg = '接口无法访问' ;
      }).finally(function(){        
        theVue.selectTableStatus = false ;
      }) ;

    } ,

    // 3. 向GPT提问
    sendQuestionToGpt: function(){
      const theVue = this ;
      if(!theVue.currentChatId) return false ;
      if(!theVue.currentQuestion) { alert('请您输入您的问题'); return false }

      theVue.currentChatList.push({
        from: 'user' ,
        content: theVue.currentQuestion ,
        type: 'message'
      }) ;

      theVue.sendQuestionStatus = true ;
      theVue.axios({
        url: '/chat' ,
        method: 'post' ,
        data: { chatId: theVue.currentChatId , query: theVue.currentQuestion }
      }).then(function(response){
        if(response.status === 200){
          const result = response.data ;
          if(result && result.success){
            theVue.currentQuestion = '' ;
            if(result.data.type === "assistant"){
              theVue.currentChatList.push({
                from: 'system' ,
                content: result.data.content && result.data.content.info ,
                type: 'message'
              }) ;
            }else{
              const theAnswerMessage = {
                from: 'system' ,
                content: '谢谢您的提问，我们为您查询到了以下的结果' ,
                chart: result.data.content ,
                question: result.data.question ,
                answerId: new Date().getTime() ,
                type: 'answer'
              } ;
              theVue.currentChatList.push(theAnswerMessage) ;

              theVue.$nextTick(function(){
                const myDfChartContainer = theVue.$refs['myDfChartContainer-' + theAnswerMessage.answerId] ;
                if(myDfChartContainer && myDfChartContainer[0]){
                    // 设置画图数据
                    myDfChartContainer[0].setChartData(theAnswerMessage.chart , {
                        searchText: theAnswerMessage.question //  搜索语句
                    });

                    // 执行画图
                    myDfChartContainer[0].drawChart() ;
                }
              }) ;
            }
          }else{
            theVue.currentChatList.push({
              from: 'system' ,
              content: '对不起，系统接口报错' ,
              type: 'message'
            }) ;
          }
        }else{
          theVue.currentChatList.push({
            from: 'system' ,
            content: '对不起，系统接口无法访问' ,
            type: 'message'
          }) ;
        }
      }).catch(function(){
        theVue.currentChatList.push({
          from: 'system' ,
          content: '对不起，系统接口无法访问' ,
          type: 'message'
        }) ;
      }).finally(function(){
        theVue.sendQuestionStatus = false ;
      }) ;
    }


    


  }
}
</script>


<style lang="css">
.body-container{position:absolute;top:0;left:0;width:100%;height:100%;}
  @import url(./assets/example.css);
</style>