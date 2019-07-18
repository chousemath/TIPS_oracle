const assert = require('assert');
const expect = require('chai').expect;
const mappings = require('../js/mappings');

const colors = {
  "검정색": 1,
  "검정투톤": 1,
  "검정": 1,
  "흰색": 2,
  "아이보리": 2,
  "흰색투톤": 2,
  "은색": 3,
  "명은색": 3,
  "은하색": 3,
  "은색투톤": 3,
  "진주색": 4,
  "베이지": 4,
  "진주투톤": 4,
  "회색": 5,
  "쥐색": 5,
  "코스모그레이": 5,
  "다크그레이": 5,
  "은회색": 5,
  "빨강색": 6,
  "빨간색": 6,
  "빨강": 6,
  "자주색": 6,
  "흑장미": 6,
  "분홍색": 6,
  "분홍": 6,
  "파랑색": 7,
  "파랑": 7,
  "청색": 7,
  "댄디블루": 7,
  "다크블루": 7,
  "하늘색": 7,
  "주황색": 8,
  "주황": 8,
  "오렌지색": 8,
  "갈색": 9,
  "갈대색": 9,
  "연금색": 9,
  "갈색투톤": 9,
  "초록색": 10,
  "녹색": 10,
  "담녹색": 10,
  "청옥색": 10,
  "연두색": 10,
  "연두": 10,
  "민트": 10,
  "노랑색": 11,
  "노란색": 11,
  "노랑": 11,
  "금색": 11,
  "금색투톤": 11,
  "노랑투톤": 11,
  "보라색": 12,
  "보라": 12
};

describe('mappings.js', () => {
  describe('#colorToNumber()', () => {
    it('should return a value of 0 for an unknown color', () => {
      expect(mappings.colorToNumber('banana')).to.equal(0);
    });
    it('should correctly pair a known color with a color code', () => {
      for (let color in colors) {
        expect(mappings.colorToNumber(color)).to.equal(colors[color]);
      }
    });
  });
});