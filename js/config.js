/*
 * CRAFTFLOW サイト設定
 * お問い合わせフォーム（Google フォーム）を作成したら、下の2つを設定してください。
 *
 *   formUrl      … フォームの「送信」→「<>（埋め込み）」に出てくる src の URL
 *                  例: https://docs.google.com/forms/d/e/xxxxxxxx/viewform?embedded=true
 *   formOpenUrl  … 新しいタブで開く用の URL（「リンク」で取得する URL）
 *
 * 空欄のままだと、問い合わせページには「フォーム準備中」と表示され、
 * 送信できるようには見えません。
 */
window.CRAFTFLOW_CONFIG = {
  formUrl: "",
  formOpenUrl: ""
};
